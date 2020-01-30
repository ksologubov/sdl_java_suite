
	/**
	 * Constructs a new SetInteriorVehicleDataResponse object
	 * @param moduleData
	 * @param success whether the request is successfully processed
	 * @param resultCode whether the request is successfully processed
	 * @deprecated use {@link SetInteriorVehicleDataResponse#SetInteriorVehicleDataResponse(Result, Boolean)}
	 */
	@Deprecated
	public SetInteriorVehicleDataResponse(@NonNull ModuleData moduleData, @NonNull Result resultCode, @NonNull Boolean success) {
		this();
		setModuleData(moduleData);
		setResultCode(resultCode);
		setSuccess(success);
	}
