
    public static final String KEY_DATA = "data";

    @SuppressWarnings("unchecked")
    public List<String> getLegacyData() {
        return (List<String>) getObject(String.class, KEY_DATA);
    }

    public void setLegacyData( List<String> data ) {
        setParameters(KEY_DATA, data);
    }