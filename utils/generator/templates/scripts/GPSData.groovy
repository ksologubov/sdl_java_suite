
    /**
     * Constructs a newly allocated GPSData object
     * @deprecated Use {@link #GPSData(@NonNull Float, @NonNull Float)()} instead
     */
    @Deprecated
    public GPSData(@NonNull Float longitudeDegrees, @NonNull Float latitudeDegrees, @NonNull Integer utcYear,
                   @NonNull Integer utcMonth, @NonNull Integer utcDay, @NonNull Integer utcHours,
                   @NonNull Integer utcMinutes, @NonNull Integer utcSeconds, @NonNull CompassDirection compassDirection,
                   @NonNull Float pdop, @NonNull Float hdop, @NonNull Float vdop, @NonNull Boolean actual,
                   @NonNull Integer satellites, @NonNull Dimension dimension, @NonNull Float altitude, @NonNull Float heading, @NonNull Float speed) {
        this();
        setLongitudeDegrees(longitudeDegrees);
        setLatitudeDegrees(latitudeDegrees);
        setUtcYear(utcYear);
        setUtcMonth(utcMonth);
        setUtcDay(utcDay);
        setUtcHours(utcHours);
        setUtcMinutes(utcMinutes);
        setUtcSeconds(utcSeconds);
        setCompassDirection(compassDirection);
        setPdop(pdop);
        setHdop(hdop);
        setVdop(vdop);
        setActual(actual);
        setSatellites(satellites);
        setDimension(dimension);
        setAltitude(altitude);
        setHeading(heading);
        setSpeed(speed);
    }
