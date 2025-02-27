from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from routes.discussion import router as discussion_router
from routes.history import router as history_router
# Create the FastAPI app
app = FastAPI()

# Add CORS middleware (optional, for frontend integration)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://leads-gen-ai.vercel.app"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include the router with the /api prefix
app.include_router(discussion_router, prefix="/api")
app.include_router(history_router, prefix="/api")

# Print all registered routes
for route in app.routes:
    print(f"Path: {route.path}, Methods: {route.methods}")
# Main function to run the app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)