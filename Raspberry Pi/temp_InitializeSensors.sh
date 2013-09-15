echo "Configuring temperature sensors for use."
echo " *Note* This only needs to be run once before launching temp_LoggingServer.py"
sudo modprobe w1-gpio
sudo modprobe w1-therm