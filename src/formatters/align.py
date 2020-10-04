# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    align.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cacharle <me@cacharle.xyz>                 +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/10/04 09:56:31 by cacharle          #+#    #+#              #
#    Updated: 2020/10/04 14:39:01 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #


import re

from formatters import formatter
import formatters.helper as helper
import formatters.regex as regex

# TODO
# align global variable in c files
# align function prototype and type declaration in header file


def align_scope(content: str, scope: str) -> str:
    """ Align content
        scope can be either local or global
          local:  for variable declarations in function
          global: for function prototypes
    """

    lines = content.split("\n")
    aligned = []
    if scope == "local":
        align_regex = (
            "^\t"
            r"(?P<type>{t})\s+"
            r"(?P<rest>{d};)$"
        )
    elif scope == "global":
        align_regex = (
            r"^(?P<type>{t})\s+"
            r"(?P<rest>{n}\(.*\);?)$"
        )
    else:
        raise RuntimeError("scope should be 'global' or 'local'")
    align_regex = align_regex.format(t=regex.TYPE, n=regex.NAME, d=regex.DECL_NAME)

    matches = [re.match(align_regex, line) for line in lines]
    aligned = [(i, match.group("type"), match.group("rest"))
               for i, (line, match) in enumerate(zip(lines, matches))
               if match is not None]

    min_alignment = max([len(type_) // 4 + 1 for _, type_, _ in aligned], default=1)

    for i, type_, rest in aligned:
        alignment = len(type_) // 4
        lines[i] = type_ + "\t" * (min_alignment - alignment) + rest
        if scope == "local":
            lines[i] = "\t" + lines[i]
    return "\n".join(lines)


@helper.local_scope
def align_local(content: str) -> str:
    return align_scope(content, scope="local")


@formatter
def align(content: str) -> str:
    """ Align the content in global and local scopes """
    content = align_scope(content, scope="global")
    content = align_local(content)
    return content
