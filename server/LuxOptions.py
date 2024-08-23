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

import subprocess
import json
import os

def serialize(lux_options, cwd):
    with open(f'{cwd}/lux_options.json', 'w') as f:
        json.dump(lux_options, f)
    if os.name == 'nt':
        subprocess.run([f'{cwd}/assets/java.exe', '-cp', f'.;{cwd}/assets/gson-2.10.1.jar;{cwd}/assets/LuxCore.jar', f'app.qwertz.luxcorepy.LuxOptionsSerializer', f'{cwd}/lux_options.json'], cwd=f"{cwd}/server")
    else:
        subprocess.run([f'chmod', '+x', f'{cwd}/assets/java'])
        subprocess.run([f'{cwd}/assets/java', '-cp', f'.;{cwd}/assets/gson-2.10.1.jar;{cwd}/assets/LuxCore.jar', f'app.qwertz.luxcorepy.LuxOptionsSerializer', f'{cwd}/lux_options.json'], cwd=f"{cwd}/server")
    # The serialized data will be in the 'luxoptions.ser' file
    with open(f'{cwd}/server/luxoptions.ser', 'rb') as f:
        serialized_data = f.read()
    os.unlink(f'{cwd}/lux_options.json')
    os.unlink(f'{cwd}/luxoptions.ser')
    print(serialized_data.hex())
    return serialized_data.hex()

def deserialize(ser_file, cwd):
    if os.name == 'nt':
        subprocess.run([f'{cwd}/assets/java.exe', '-cp', f'.;{cwd}/assets/gson-2.10.1.jar;{cwd}/assets/LuxCore.jar', f'app.qwertz.luxcorepy.LuxOptionsDeserializer', f'{ser_file}'], cwd=f"{cwd}/server")
    else:
        subprocess.run([f'chmod', '+x', f'{cwd}/assets/java'])
        subprocess.run([f'{cwd}/assets/java', '-cp', f'.;{cwd}/assets/gson-2.10.1.jar;{cwd}/assets/LuxCore.jar', f'app.qwertz.luxcorepy.LuxOptionsSerializer', f'{ser_file}'], cwd=f"{cwd}/server")
    # The serialized data will be in the 'luxoptions.ser' file
    with open(f'{cwd}/server/luxoptions.ser', 'rb') as f:
        serialized_data = f.read()
    os.unlink(f'{cwd}/luxoptions.ser') 
    print(serialized_data.hex())
    return serialized_data.hex()