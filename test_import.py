import sys, os
sys.path.append(os.path.abspath("src"))

import eventsystem.events as evt

print("MODULE:", evt)
print("LOADED FROM:", evt.__file__)
print("CONTENTS:", dir(evt))
