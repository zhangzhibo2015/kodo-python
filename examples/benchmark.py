#! /usr/bin/env python
# encoding: utf-8

import time
import os
import sys
import argparse
import pykodo as kodo


def run_coding_test(algorithm, field, symbols, symbol_size):
    """Run a timed encoding and decoding benchmark."""
    # First, we measure the combined setup time for the encoder and decoder
    start = time.clock()
    encoder_factory = kodo.encoder_factory(
        algorithm=algorithm,
        field=field,
        max_symbols=symbols,
        max_symbol_size=symbol_size)

    decoder_factory = kodo.decoder_factory(
        algorithm=algorithm,
        field=field,
        max_symbols=symbols,
        max_symbol_size=symbol_size)

    encoder = encoder_factory.build()
    decoder = decoder_factory.build()

    # Stop the setup timer
    stop = time.clock()
    # Calculate interval in microseconds
    setup_time = 1e6 * (stop - start)

    # We measure pure coding, so we always turn off the systematic mode
    if 'set_systematic_off' in dir(encoder):
        encoder.set_systematic_off()

    # Create random data to encode
    data_in = os.urandom(encoder.block_size())

    # The generated payloads will be stored in this list
    payloads = []

    # Generate an ample number of coded symbols (considering kodo_binary)
    payload_count = 2 * symbols

    # Start the encoding timer
    start = time.clock()

    # Copy the input data to the encoder
    encoder.set_const_symbols(data_in)

    # Generate coded symbols with the encoder
    for i in range(payload_count):
        payload = encoder.write_payload()
        payloads.append(payload)

    # Stop the encoding timer
    stop = time.clock()
    # Calculate interval in microseconds
    encoding_time = 1e6 * (stop - start)

    # Calculate the encoding rate in megabytes / seconds
    encoded_bytes = payload_count * symbol_size
    encoding_rate = encoded_bytes / encoding_time

    # Start the decoding timer
    start = time.clock()

    # Feed the coded symbols to the decoder
    for i in range(payload_count):
        if decoder.is_complete():
            break
        decoder.read_payload(payloads[i])

    # Copy the symbols from the decoder
    data_out = decoder.copy_from_symbols()

    # Stop the decoding timer
    stop = time.clock()
    # Calculate interval in microseconds
    decoding_time = 1e6 * (stop - start)

    # Calculate the decoding rate in megabytes / seconds
    decoded_bytes = symbols * symbol_size
    decoding_rate = decoded_bytes / decoding_time

    if data_out == data_in:
        success = True
    else:
        success = False

    print("Setup time: {} microsec".format(setup_time))
    print("Encoding time: {} microsec".format(encoding_time))
    print("Decoding time: {} microsec".format(decoding_time))

    return (success, encoding_rate, decoding_rate)


def main():
    parser = argparse.ArgumentParser(description=run_coding_test.__doc__)

    # Disable the algorithms that do not work with the benchmark code
    algorithms = list(kodo.algorithms)
    algorithms.remove(kodo.no_code)
    algorithms.remove(kodo.sparse_full_vector)

    parser.add_argument(
        '--algorithm',
        type=str,
        help='The algorithm to use',
        choices=algorithms,
        default=kodo.full_vector)

    parser.add_argument(
        '--field',
        type=str,
        help='The finite field to use',
        choices=kodo.fields,
        default=kodo.binary8)

    parser.add_argument(
        '--symbols',
        type=int,
        help='The number of symbols',
        default=16)

    parser.add_argument(
        '--symbol_size',
        type=int,
        help='The size of each symbol',
        default=1600)

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Run without the actual benchmark.')

    args = parser.parse_args()

    if args.dry_run:
        sys.exit(0)

    print("Algorithm: {} / Finite field: {}".format(
        args.algorithm, args.field))

    print("Symbols: {} / Symbol size: {}".format(
        args.symbols, args.symbol_size))

    decoding_success, encoding_rate, decoding_rate = run_coding_test(
        args.algorithm,
        args.field,
        args.symbols,
        args.symbol_size)

    print("Encoding rate: {} MB/s".format(encoding_rate))
    print("Decoding rate: {} MB/s".format(decoding_rate))

    if decoding_success:
        print("Data decoded correctly.")
    else:
        print("Decoding failed.")


if __name__ == "__main__":
    main()
