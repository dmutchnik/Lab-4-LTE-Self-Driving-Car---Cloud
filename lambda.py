import json
import logging
import boto3

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Boto3 IoT client
iot_client = boto3.client('iot-data', region_name='us-east-1')

def lambda_handler(event, context):
    logger.info(f"Received raw event: {event}")

    # Step 1: Parse incoming message (if it's a string)
    if isinstance(event, str):
        try:
            event = json.loads(event)
        except json.JSONDecodeError:
            logger.error("Failed to parse event string as JSON.")
            return {"statusCode": 400, "body": "Invalid input format"}

    # Step 2: Handle single-record or list-of-records
    records = event if isinstance(event, list) else [event]

    max_co2 = 0.0
    vehicle_id = None

    for record in records:
        try:
            co2 = float(record['vehicle_CO2'])
            vid = record['vehicle_id']
            logger.info(f"Processing: vehicle_id={vid}, CO2={co2}")
        except Exception as e:
            logger.warning(f"Skipping record due to error: {e}")
            continue

        if co2 > max_co2:
            max_co2 = co2
            vehicle_id = vid

    if not vehicle_id:
        logger.warning("No valid records found.")
        return {"statusCode": 400, "body": "No valid data to process"}

    # Construct MQTT message and topic
    topic = f"vehicles/{vehicle_id.replace('veh', '')}/analysis"
    message = {
        "max_CO2": max_co2,
        "vehicle_id": vehicle_id
    }

    logger.info(f"Publishing to {topic}: {json.dumps(message)}")
    iot_client.publish(
        topic=topic,
        qos=1,
        payload=json.dumps(message)
    )

    return {
        "statusCode": 200,
        "body": f"Published max CO2 for vehicle {vehicle_id}"
    }