{% extends "base_template.java" %}
{% block body %}
public class {{class_name}} extends {{extends_class}} {
    {%- if params is defined %}
    {%- for p in params %}
    {%- if p.description is defined and p.description|length or p.since is defined or p.see is defined %}
    /**
     {%- if p.deprecated is not none %}
     * @deprecated
     {%- endif %}
     {%- if p.description is defined %}
     {%- for d in p.description %}
     * {{d}}
     {%- endfor %}{% endif -%}
     {%- if p.description is defined and (p.since is defined or p.see is defined) %}
     *
     {%- endif %}
     {%- if p.since is defined %}
     * @since SmartDeviceLink {{p.since}}
     {%- endif %}
     {%- if p.see is defined %}
     * @see {{p.see}}
     {%- endif %}
     */
    {%- endif %}
    {%- if p.name is defined %}
    private {% if p.modifier is defined %}{{p.modifier}} {% endif %}{{p.return_type}} {{p.name}}{% if p.value is defined %} = {{p.value}}{% endif %};
    {%- else %}
    public static final String {{p.key}} = "{{p.origin}}";
    {%- endif %}
    {%- endfor %}
    {%- endif %}

    /**
     * Constructs a newly allocated {{class_name}} object
     */
    public {{class_name}}() { }

    /**
     * Constructs a newly allocated {{class_name}} object indicated by the Hashtable parameter
     * @param hash The Hashtable to use
     */
    public {{class_name}}(Hashtable<String, Object> hash) {
        super(hash);
    }
    {%- if params is defined %}
    {%- set constructor = [] %}
    {%- for p in params|selectattr('mandatory') %}{{ constructor.append('@NonNull ' + p.return_type + ' ' + p.last) or '' }}
    {%- endfor %}
    {%- if constructor|length > 0 %}

    /**
     * Constructs a newly allocated {{class_name}} object
     *
     {% for p in params|selectattr('mandatory') -%}
     {% if p.param_doc is not defined -%}
     * @param {{p.last}}
     {% else -%}
     {% set l = p.last|length + 8 -%}
     * {% for v in p.param_doc -%}
     {% if loop.index == 1 -%}
     @param {{p.last}} {{v}}
     {% else -%}
     * {{v|indent(l,True)}}
     {% endif -%} {% endfor -%}
     {% endif -%}
     {% endfor -%}
     */
    public {{class_name}}({{ constructor|join(', ') }}) {
        this();
        {%- for p in params|selectattr('mandatory') %}
        set{{p.title}}({{p.last}});
        {%- endfor %}
    }
    {%- endif %}
    {%- endif %}

    {%- if params is defined %}
    {%- for p in params|rejectattr('name') %}

     /**
     * Gets the {{p.origin}}.
     *
     {% if p.param_doc is not defined -%}
     * @return {{p.return_type}}
    {% else -%}
    {% set l = p.last|length + 8 -%}
     * {% for v in p.param_doc -%}
    {% if loop.index == 1 -%}
     @return {{p.return_type}} {{v}}
     {% else -%}
      * {{v|indent(l,True)}}
     {% endif -%} {% endfor -%}
     {% endif -%}
     */
    {%- if p.SuppressWarnings is defined %}
    @SuppressWarnings("{{p.SuppressWarnings}}")
    {%- endif %}
    public {{p.return_type}} get{{p.title}}() {
        {%- if p.return_type in ['String', 'Boolean', 'Integer'] %}
        return get{{p.return_type}}({{p.key}});
        {%- else %}
        {%- set clazz = p.return_type %}
        {%- if p.return_type.startswith('List')%}{%set clazz = p.return_type[5:-1]%}{% endif %}
        return ({{p.return_type}}) getObject({{clazz}}.class, {{p.key}});
        {%- endif %}
    }

    /**
     * Sets the {{p.origin}}.
     {%- if p.description is defined %}
     {%- for d in p.description %}
     * {{d}}
     {%- endfor %}{%- endif %}
     *
     {% if p.param_doc is not defined -%}
     * @param {{p.last}}
     {% else -%}
     {% set l = p.last|length + 8 -%}
     * {% for v in p.param_doc -%}
     {% if loop.index == 1 -%}
     @param {{p.last}} {{v}}
     {% else -%}
     * {{v|indent(l,True)}}
     {% endif -%} {% endfor -%}
     {% endif -%}
     */
    public void set{{p.title}}({% if p.mandatory %}@NonNull {% endif %}{{p.return_type}} {{p.last}}) {
        setValue({{p.key}}, {{p.last}});
    }

    {%- endfor %}
    {%- endif %}

    {%- if scripts is defined %}

    {%- for s in scripts %}
{{s}}
    {% endfor %}
    {%- endif %}
}
{% endblock -%}