{% extends "base_template.java" %}

public enum {{enumname}} {
    {%- for param in params %}
        {{param}},
    {%- endfor %};

    /**
     * Convert String to {{enumname}}
     * @param value String
     * @return {{enumname}}
     */
    public static {{enumname}} valueForString(String value) {
        try{
            return valueOf(value);
        }catch(Exception e){
            return null;
        }
    }
}