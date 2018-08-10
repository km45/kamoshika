# -*- coding: utf-8 -*-
import typing

# PostQueryStream example:
#     [
#         {
#             # host1
#             'a.txt': b'aaa',
#             'b.txt': b'bbb'
#         }, {
#             # host2
#             'a.txt': b'aaa',
#             'b.txt': b'ddd'
#         }
#     ]
PostQueryStream = typing.List[typing.Dict[str, bytes]]
