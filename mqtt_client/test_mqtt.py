import json
import ssl
import sys
import socket
import random
import time
import paho.mqtt.client as mqtt

BROKER = '10.100.13.230'
PORT = 8884

CA_CERT_FILE = '../certs/mqtt/certs_issued/mqtt-broker-showcase-robot-test-003/ca-chain.cert.pem'
CERT_FILE = '../certs/mqtt/certs_issued/mqtt-broker-showcase-robot-test-004/mqtt-broker-showcase-robot-test-004.cert.pem'
KEY_FILE = '../certs/mqtt/certs_issued/mqtt-broker-showcase-robot-test-004/mqtt-broker-showcase-robot-test-004.key.pem'
TOPIC = 'test/test'


def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))


def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
    print(string)


def test_certificate_chain():
    context = ssl.create_default_context(cafile=CA_CERT_FILE)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            with context.wrap_socket(sock, server_hostname='localhost') as ssock:
                ssock.settimeout(10)
                ssock.bind(('localhost', 0))
                ssock.listen(5)
    except ssl.SSLError as e:
        print(f"Certificate chain verification failed: {e}")
    else:
        print("Certificate chain verified successfully.")


if __name__ == "__main__":
    test_certificate_chain()

    # Create Client with Websockets transport
    mqttc = mqtt.Client('mqtt-client', transport='websockets')
    mqttc.on_log = on_log

    mqttc.tls_set(ca_certs=CA_CERT_FILE, certfile=CERT_FILE, keyfile=KEY_FILE, tls_version=ssl.PROTOCOL_TLSv1_2)
    # mqttc.tls_insecure_set(True)  # for Self-Signed Certificates

    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe
    # Uncomment to enable debug messages
    mqttc.connect(BROKER, PORT, 60)
    mqttc.subscribe(TOPIC, 0)

    try:
        # Start the MQTT network loop to handle incoming/outgoing messages
        mqttc.loop_start()

        while True:  # Run an infinite loop
            # Publish JSON data to the specified topic
            data = {
                "key1": random.uniform(10, 15),
                "key2": random.uniform(120, 125),
                "key3": random.uniform(160, 185)
            }
            json_data = json.dumps(data)
            mqttc.publish(TOPIC, payload=json_data)

            # Wait for 5 seconds before publishing the next message
            time.sleep(5)

    except KeyboardInterrupt:
        print('CTRL+C Pressed')
        # Cleanly stop the MQTT network loop and disconnect from the broker
        mqttc.loop_stop()
        mqttc.disconnect()
        sys.exit()
