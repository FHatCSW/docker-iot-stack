# docker-iot-stack

```
docker run -it --rm -v "%cd%/mosquitto/config:/mosquitto/config" eclipse-mosquitto mosquitto_passwd -U /mosquitto/config/passwd
```

## Coverting .p12 to certificate and key

### Extact the certificate
```
openssl pkcs12 -in yourfile.p12 -clcerts -nokeys -out certificate.pem
```

### Extract the key
```
openssl pkcs12 -in yourfile.p12 -nocerts -nodes -out privatekey.pem
```