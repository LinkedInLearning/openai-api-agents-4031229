from .server import serve


def main():
    """MCP Weather Server - Weather forecast and conditions functionality for MCP"""
    import argparse
    import asyncio

    parser = argparse.ArgumentParser(
        description="give a model the ability to get weather forecasts and current conditions"
    )

    args = parser.parse_args()
    asyncio.run(serve())


if __name__ == "__main__":
    main() 