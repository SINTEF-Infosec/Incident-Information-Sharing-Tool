from django import template
from django.template.defaulttags import register

register = template.Library()

@register.filter(name='get_language')
def get_language(language_key):
    if(language_key == 'nb_NO'):
        return 'Norwegian'
    else:
        return 'English'

@register.filter(name='get_status')
def get_status(status):
    if(status == 'resolved'):
        return '<i class="fa fa-check resolved"></i> Resolved'
    else:
        return '<i class="fa fa-exclamation-triangle unresolved"></i> Unresolved'

@register.filter(name='get_impact')
def get_impact(impact):
    if 0.8 <= impact:
        return '<span class="label label-danger">%.2f - High</span>' % impact
    elif 0.4 < impact < 0.8:
        return '<span class="label label-warning">%.2f - Medium</span>' % impact
    else:
        return '<span class="label label-success">%.2f - Low</span>' % impact

def _get_class_for_field(field, tlp_fields):
    tlp_value = ''
    
    if tlp_fields:
        for item in tlp_fields:
            if item.field == field.name:
                tlp_value = item.value
                break
    
    if tlp_value != '':
        return tlp_value
    else:
        return 'deactive'
        
@register.filter(name='print_form_field')
def print_form_field(field, tlp_fields):    
    value = _get_class_for_field(field, tlp_fields)
    checked = 'checked'
    
    field_html = '<div class="input-group tlp">'
    
    field_html += field.as_widget(attrs={'class': 'form-control'})
    field_html += '<span class="input-group-addon ' + value + ' btn tlp-indicator"><span class="red circle"></span><span class="amber circle"></span><span class="green circle"></span></span>'
    field_html += '<div class="tlp-selector collapse">'
    field_html +=   '<h3>TLP value</h3>'
    field_html +=   '<label class="red"><input type="radio" name="tlp-' + field.name + '" value="red" ' + (checked if value == 'red' else '') + '>Red</label><br/><label class="amber"><input type="radio" name="tlp-' + field.name + '" value="amber" ' + (checked if value == 'amber' else '') + '>Amber</label><br/><label class="green"><input type="radio" name="tlp-' + field.name + '" value="green" ' + (checked if value == 'green' else '') + '>Green</label><br/><label class="white"><input type="radio" name="tlp-' + field.name + '" value="white" ' + (checked if value == 'white' else '') + '>White</label></div>'
    
    field_html += '</div>'
    
    return field_html

@register.filter(name='field_with_button')
def field_with_button(field, button_text):
    field_html = '<div class="input-group">'
    
    field_html += field.as_widget(attrs={'class': 'form-control'})
    field_html += '<span class="input-group-addon btn">' + button_text + '</span>'
    
    field_html += '</div>'
    
    return field_html

@register.filter(name='tlp_for_field')
def tlp_for_field(field, tlp_fields):
    tlp_value = ''
    
    if tlp_fields:
        for item in tlp_fields:
            if item.field == field:
                tlp_value = item.value
                break
    
    return tlp_value

@register.filter(name='tlp_map_to_list')
def tlp_map_to_list(map):
    names = []
    
    for item in map:
        names.append(item.field)
    
    print(names)
    
    return names