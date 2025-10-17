# Local Popularity Map Feature

## Overview
This feature implements a geographic map showing trending movies by region, allowing users to discover what's popular around them or in other regions worldwide.

## User Story Implementation
**As a User**, I want to see a map showing which movies of the GT Movie Store are trending (or most purchased) in different geographic areas, so I can discover what's popular around me or in other regions.

## Completion Steps Verification

### a) ✅ Log in or register an account
- The map feature is only accessible to authenticated users
- Navigate to `/accounts/login/` or `/accounts/signup/` to create an account

### b) ✅ Navigate to the "Local Popularity Map" page
- After logging in, click on the "🗺️ Trending Map" link in the navigation bar
- Or navigate directly to `/cart/map/`

### c) ✅ Verify that the map loads correctly with regional boundaries or markers
- Interactive map displays 6 major regions: North America, Europe, Asia, South America, Africa, and Oceania
- Each region has a red circular marker showing its location
- Map uses OpenStreetMap tiles for geographic boundaries

### d) ✅ Confirm that movies with high purchase/view counts are displayed as trending in at least one region
- Click on any region marker to see a popup with trending movie count
- Sample data has been populated with 63+ orders across all regions
- Each region displays top 3-5 trending movies based on actual purchase data

### e) ✅ Select a specific region on the map
- Click on any red marker on the map
- Use the "Set Your Location" dropdown to select a region
- Submit the form to focus on that region

### f) ✅ Verify that the region's top trending movies are listed (titles, counts, etc.)
- Right panel displays "Regional Trending Movies" when a region is selected
- Shows movie names, purchase counts, and total quantities
- Rankings display from #1 to #5 based on popularity

### g) ✅ Compare this list with your own recent purchases
- Right panel shows "Your Recent Purchases" section
- Lists all movies you've purchased with quantities and dates
- Allows comparison between personal preferences and regional trends

## Features Implemented

### 1. Database Schema Updates
- Added `region`, `latitude`, and `longitude` fields to the Order model
- Tracks geographic location for each purchase
- Migration created and applied successfully

### 2. Backend Views & API
- **`map_view()`**: Renders the map page with user's purchase history
- **`map_data_api()`**: JSON API endpoint providing trending data by region
- **`set_location()`**: Allows users to set their preferred region
- **Updated `purchase()`**: Now captures user's region when making purchases

### 3. Frontend Map Interface
- Interactive Leaflet.js map with OpenStreetMap tiles
- 6 regional markers covering major geographic areas worldwide
- Clickable markers showing region name and trending movie count
- Real-time data loading via AJAX from the API endpoint

### 4. User Interface Components
- **Location Selector**: Dropdown to select and save user's region
- **Regional Data Panel**: Displays top trending movies for selected region
- **User Purchases Panel**: Shows personal purchase history for comparison
- **Responsive Design**: Mobile-friendly layout using Bootstrap 5

### 5. Sample Data Generation
- Management command `populate_regional_data` created
- Generates realistic sample data across all 6 regions
- Creates 63 sample orders with varying movie purchases
- Demonstrates the feature with meaningful data

### 6. Navigation Integration
- Added "Trending Map" link to main navigation bar
- Only visible to authenticated users
- Icon-enhanced for better visibility

## Technical Stack
- **Backend**: Django views with JSON API endpoints
- **Database**: SQLite with geographic fields (latitude, longitude, region)
- **Frontend**: Leaflet.js for interactive maps
- **Maps**: OpenStreetMap tiles
- **Styling**: Bootstrap 5 + Custom CSS
- **AJAX**: Fetch API for dynamic data loading

## How to Use

1. **Start the server** (if not already running):
   ```bash
   source venv/bin/activate
   python manage.py runserver
   ```

2. **Access the application**:
   - Open browser to http://localhost:8000

3. **Login or create an account**:
   - Use existing credentials or sign up for a new account
   - Demo user: username: `demo_user`, password: `demo123`

4. **Navigate to the map**:
   - Click "🗺️ Trending Map" in the navigation bar

5. **Explore regional trends**:
   - Click on red markers to see trending movies
   - Use the location selector to set your region
   - Compare trending movies with your own purchases

6. **Make purchases** (to see personal data):
   - Browse movies at `/movies/`
   - Add movies to cart
   - Complete purchase (location will be tracked)

## API Endpoints

### GET `/cart/api/map-data/`
Returns trending movie data for all regions.

**Response format**:
```json
{
  "regions": [
    {
      "region": "North America",
      "latitude": 39.8283,
      "longitude": -98.5795,
      "trending_movies": [
        {
          "movie_id": 1,
          "movie_name": "Inception",
          "purchase_count": 5,
          "total_quantity": 12
        }
      ]
    }
  ]
}
```

### POST `/cart/set-location/`
Sets user's preferred region in session.

**Parameters**:
- `region`: Region name
- `latitude`: (Optional) Latitude coordinate
- `longitude`: (Optional) Longitude coordinate

## Files Modified/Created

### Modified Files:
- `cart/models.py` - Added geographic fields to Order model
- `cart/views.py` - Added map view and API endpoints
- `cart/urls.py` - Added URL routing for map pages
- `moviesstore/templates/base.html` - Added navigation link

### New Files:
- `cart/templates/cart/map.html` - Map page template
- `cart/migrations/0003_order_latitude_order_longitude_order_region.py` - Database migration
- `cart/management/commands/populate_regional_data.py` - Sample data generator

## Future Enhancements
- Real IP-based geolocation
- More granular regions (cities, states)
- Heat map visualization
- Time-based trending (weekly, monthly)
- Export trending reports
- Social sharing of regional favorites

## Testing Notes
- Sample data includes 63 orders across 6 regions
- All regions have trending data
- Demo user created for easy testing
- Map works on mobile and desktop browsers

## Support
For issues or questions, refer to the Django documentation or the Leaflet.js documentation.

---
**Feature Status**: ✅ Complete and Functional
**Date Implemented**: October 17, 2025

