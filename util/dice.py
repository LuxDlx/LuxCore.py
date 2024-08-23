# Copyright (C) 2024  QWERTZexe

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 2.1 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

######################################################

import random

def simulate(attackerarmies, defenderarmies):
    randomifier = random.randint(0,4)
    if randomifier == 0 or randomifier == 1:
        return (attackerarmies-1, defenderarmies-1)
    elif randomifier == 2 or randomifier == 3:
        return (attackerarmies, defenderarmies-1)
    elif randomifier == 4:
        return (attackerarmies-1, defenderarmies)