
    public static final String KEY_DATA = "data";

    private String body;
    private Headers headers;

    @SuppressWarnings("unchecked")
    public List<String> getLegacyData() {
        return (List<String>) getObject(String.class, KEY_DATA);
    }

    public String getBody(){
        return this.body;
    }

    public void setBody(String body) {
        this.body = body;
    }

    public void setHeaders(Headers header) {
        this.headers = header;
    }

    public Headers getHeader() {
        return this.headers;
    }
