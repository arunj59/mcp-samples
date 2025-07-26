import asyncio
from tools.indian_railways_tools import search_trains

async def main():
    # Test search_trains with sample route
    print("\nTesting Train Search:")
    result = await search_trains('NDLS', 'BCT', '25-04-2024')
    print(result)

if __name__ == "__main__":
    asyncio.run(main()) 