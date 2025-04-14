import boto3
import os

iot = boto3.client('iot', region_name='us-east-1')

THING_GROUP_NAME = "MyThingGroup"
POLICY_NAME = "MyIoTPolicy"
KEYS_DIR = "./keys"

# Make sure the ./keys directory exists
os.makedirs(KEYS_DIR, exist_ok=True)

def create_and_register_thing(thing_name):
    # Create Thing
    response = iot.create_thing(thingName=thing_name)
    print(f"Thing created: {thing_name}")

    # Create cert + key
    cert_response = iot.create_keys_and_certificate(setAsActive=True)
    cert_arn = cert_response['certificateArn']
    cert_id = cert_response['certificateId']
    print(f"Certificate created: {cert_id}")

    # Save keys to file
    device_id = thing_name.split('_')[-1]
    os.makedirs("./keys", exist_ok=True)
    with open(f"./keys/device{device_id}.certificate.pem", "w") as f:
        f.write(cert_response['certificatePem'])
    with open(f"./keys/device{device_id}.private.pem", "w") as f:
        f.write(cert_response['keyPair']['PrivateKey'])
    with open(f"./keys/device{device_id}.public.pem", "w") as f:
        f.write(cert_response['keyPair']['PublicKey'])

    # Attach policy
    try:
        iot.attach_policy(
            policyName=POLICY_NAME,
            target=cert_arn
        )
        print(f"Policy {POLICY_NAME} attached to cert.")
    except iot.exceptions.ResourceAlreadyExistsException:
        print("Policy already attached.")

    # Attach cert to Thing
    try:
        iot.attach_thing_principal(
            thingName=thing_name,
            principal=cert_arn
        )
        print(f"Principal (cert) attached to {thing_name}")
    except iot.exceptions.ResourceAlreadyExistsException:
        print("Cert already attached to Thing.")

    # Add to Thing Group
    iot.add_thing_to_thing_group(
        thingGroupName=THING_GROUP_NAME,
        thingName=thing_name
    )
    print(f"Thing added to group {THING_GROUP_NAME}")


# === Create Multiple Things ===
for i in range(5):  # Adjust as needed
    thing_name = f"MyIoTDevice_{i}"
    create_and_register_thing(thing_name)
