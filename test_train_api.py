import asyncio
from tools.indian_railways_tools import get_train_info

async def main():
    train_number = "12051"  # Example train number
    
    print("\nTesting Train Info:")
    result = await get_train_info(train_number)
    print(result)

if __name__ == "__main__":
    asyncio.run(main()) 