# Solution to coding assignment – Weather Microservice

## Task description
Implement a minimal but stable microservice that will serve as a foundation for a long-lived system. The service should:
- Save the temperature for a specific city (e.g., Kyiv) every hour 
- Allow querying the historical temperature for a given day
- Require an x-token header with a 32-character token for all requests (acts as a simple bot filter)
- Respond with JSON in all cases, including errors
- Be containerized and run via Docker

Any weather API provider can be used. I've used [OpenWeatherMap API](https://openweathermap.org/api).

## Solution description
My solution includes the following stack:
1. Django, DRF
2. Celery, Celery Beat
3. PostgreSQL
4. Redis
5. Docker, docker-compose

### Launch instructions
To start the app you need to:
1. Clone the repository:
    ```
    https://github.com/quietix/test-task-weather-tracker.git
    cd test-task-weather-tracker
    ```
2. Configure `.env` (you can use `.env.example` as a template)
3. Run service using Docker:
    ```
    docker-compose up --build
    ```

### API Usage
1. There's single endpoint: `GET /statistics/<YYYY-MM-DD>` \
    It returns the temperature records for a given day.
2. Add `x-token` header to the request. Doesn't matter what you add, only that it's length is 32 chars
3. Response:
    ```json
    [
      {
        "city": "<CITY>",
        "temperature": <temperature_in_celsius_float>,
        "local_time": "yyyy-mm-dd hh:mm:ss"
      },
      ...
      {
        "city": "<CITY>",
        "temperature": <temperature_in_celsius_float>,
        "local_time": "yyyy-mm-dd hh:mm:ss"
      }
    ]
    ```
