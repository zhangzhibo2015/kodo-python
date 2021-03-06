// Copyright Steinwurf ApS 2015.
// Distributed under the "STEINWURF RESEARCH LICENSE 1.0".
// See accompanying file LICENSE.rst or
// http://www.steinwurf.com/licensing

#include <kodo/rlnc/perpetual_codes.hpp>

#include "create_helpers.hpp"

namespace kodo_python
{
    template<>
    struct extra_encoder_methods<kodo::rlnc::perpetual_encoder>
    {
        template<class EncoderClass>
        extra_encoder_methods(EncoderClass& encoder_class)
        {
            using boost::python::arg;

            encoder_class
            .def("pseudo_systematic",
                &EncoderClass::wrapped_type::pseudo_systematic,
                "Get the pseudo-systematic property of the generator.\n\n"
                "\t:returns: The current setting for pseudo-systematic.\n"
            )
            .def("set_pseudo_systematic",
                &EncoderClass::wrapped_type::set_pseudo_systematic,
                arg("pseudo_systematic"),
                "Set the pseudo-systematic property of the generator.\n\n"
                "\t:param pseudo_systematic: The new setting for "
                "pseudo-systematic\n"
            )
            .def("pre_charging",
                &EncoderClass::wrapped_type::pre_charging,
                "Get the pre-charging property of the generator.\n\n"
                "\t:returns: The current setting for pseudo-systematic.\n"
            )
            .def("set_pre_charging",
                &EncoderClass::wrapped_type::set_pre_charging,
                arg("pre_charging"),
                "Set the pre-charging property of the generator.\n\n"
                "\t:param pre_charging: The current setting for pre-charging.\n"
            )
            .def("width", &EncoderClass::wrapped_type::width,
                "Get the width.\n\n"
                "\t:returns: The width used by the generator.\n"
            )
            .def("set_width", &EncoderClass::wrapped_type::set_width,
                arg("width"),
                "Set the number of non-zero coefficients after the pivot. "
                "Width ratio is recalculated from this value.\n\n"
                "\t:param width: The width.\n"
            )
            .def("width_ratio", &EncoderClass::wrapped_type::width_ratio,
                "Get the ratio that is used to calculate the width.\n\n"
                "\t:returns: The width ratio of the generator.\n"
            )
            .def("set_width_ratio",
                &EncoderClass::wrapped_type::set_width_ratio,
                arg("width_ratio"),
                "Set the ratio that is used to calculate the number of "
                "non-zero coefficients after the pivot (i.e. the width).\n\n"
                "\t:param width_ratio: The width ratio.\n"
            );
        }
    };

    void create_perpertual_stacks()
    {
        using namespace kodo::rlnc;

        create_encoder<perpetual_encoder>("Perpetual");
        create_decoder<perpetual_decoder>("Perpetual");
    }
}
