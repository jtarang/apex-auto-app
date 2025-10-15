from fastmcp import FastMCP
import httpx

API_URL = "http://127.0.0.1:8000"

mcp = FastMCP(
    name="apex-auto-mcp",
    instructions="MCP server for Apex Auto Inventory",
)

@mcp.tool
async def create_vehicle(vehicle_data: dict):
    """Create a new vehicle. vehicle_data should include the fields required by VehicleCreate."""
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{API_URL}/vehicles/", json=vehicle_data)
        if resp.status_code != 201:
            return {"error": resp.json()}
        return resp.json()

@mcp.tool
async def list_vehicles(skip: int = 0, limit: int = 100):
    """List vehicles with optional skip/limit pagination."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{API_URL}/vehicles/", params={"skip": skip, "limit": limit})
        return resp.json()

@mcp.tool
async def get_vehicle(vehicle_id: int):
    """Retrieve a vehicle by ID."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{API_URL}/vehicles/{vehicle_id}")
        if resp.status_code == 404:
            return {"error": "Vehicle not found"}
        return resp.json()

@mcp.tool
async def update_vehicle(vehicle_id: int, vehicle_data: dict):
    """Update a vehicle by ID. vehicle_data should include fields allowed in VehicleUpdate."""
    async with httpx.AsyncClient() as client:
        resp = await client.patch(f"{API_URL}/vehicles/{vehicle_id}", json=vehicle_data)
        if resp.status_code == 404:
            return {"error": "Vehicle not found"}
        return resp.json()

@mcp.tool
async def delete_vehicle(vehicle_id: int):
    """Delete a vehicle by ID."""
    async with httpx.AsyncClient() as client:
        resp = await client.delete(f"{API_URL}/vehicles/{vehicle_id}")
        if resp.status_code == 404:
            return {"error": "Vehicle not found"}
        return {"status": "deleted"} if resp.status_code == 204 else resp.json()

if __name__ == "__main__":
    mcp.run(transport="http", port=8001)
