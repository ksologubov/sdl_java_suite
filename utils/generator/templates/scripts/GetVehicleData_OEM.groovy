    /**
     * Sets a boolean value for OEM Custom VehicleData.
     * @param vehicleDataName a String value
     * @param vehicleDataState a boolean value
     */
    public void setOEMCustomVehicleData(String vehicleDataName, Boolean vehicleDataState){
        setParameters(vehicleDataName, vehicleDataState);
    }

    /**
     * Gets a boolean value for OEM Custom VehicleData.
     * @return a Boolean value.
     */
    public Boolean getOEMCustomVehicleData(String vehicleDataName){
        return getBoolean(vehicleDataName);
    }