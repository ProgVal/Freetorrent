# -*- coding: utf8 -*-

# Copyright (c) 2010, Valentin Lorentz
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the University of California, Berkeley nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE REGENTS AND CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import hashlib
from common import db
from common.lib.pesto import cookie

def getUserFromCookies(cookies):
    if not cookies.has_key('uid') or not cookies.has_key('passwdhash'):
        return User()
    return User(cookies['uid'].value, cookies['passwdhash'].value)

users = {}
def User(id=0, passwdhash=None):
    global users
    if not users.has_key(id):
        users.update({id: _User(id, passwdhash)})
    return users[id]
class _User:
    def __init__(self, id, passwdhash):
        self.__class__.__name__ = 'User'
        cursor = db.conn.cursor()
        if passwdhash is not None:
            cursor.execute("""SELECT name, passwdhash FROM users
                           WHERE id=? AND passwdhash=?""",
                           (id, passwdhash))
        else:
            cursor.execute("""SELECT name, passwdhash FROM users
                           WHERE id=?""",
                           (id,))

        row = cursor.fetchone()
        if row is None:
            self.id = 0
            self.name = 'anonyme'
            self.passwdhash = ''
        else:
            self.id = id
            self.name, self.passwdhash = row