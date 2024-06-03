# Order Management System

## API Endpoints

### Get Order by ID
**URL**: `/api/order/<order_id>`

**Method**: `POST`

**Headers**:
- `Authorization`: Basic Auth (username:password)

**Response**:
- `200 OK`: `{ "order_id": 1, "status": "pending" }`
- `404 Not Found`: `{ "error": "Order not found" }`

## How to Run

1. Clone the repository.
2. Create a virtual environment and activate it.
3. Install the dependencies.
4. Run `docker-compose up`.
5. Access the admin panel at `http://localhost:5000/admin`.

## Authorize Admin

To authorize the admin, use the Flask-Security module. You can set up the admin user using the command line or Flask shell.

## JSON-RPC protocol for receiving order information

### Method:

- **get_order_info**

### Parameters:

- **order_id**: int - номер заказа, для которого требуется получить информацию.

### An example of a request:

```json
{
    "method": "get_order_info",
    "params": {
        "order_id": 123
    },
    "id": 1
}