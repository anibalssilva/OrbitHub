import sys
sys.path.append('.')

from app.data_access import filter_satellites

result = filter_satellites(limit=1)
print(f"Number of results: {len(result)}")
if result:
    print(f"Fields in result: {list(result[0].keys())}")
    print(f"First result: {result[0]}")

