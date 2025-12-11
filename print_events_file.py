with open("src/eventsystem/events.py", "rb") as f:
    content = f.read()

print("RAW BYTES:", content)
print("\nDECODED:")
print(content.decode("utf-8", errors="replace"))
