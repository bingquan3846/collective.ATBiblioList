//
// Based on ATReferenceBrowserWidget by Danny Bloemendaal
//

// function to open the popup window
function bibrefbrowser_openBrowser(path, fieldName, at_uid)
{
    window.open(path + '/popup_bibrefbrowser?fieldName=' + fieldName + '&at_uid=' + at_uid,'popupbrowser_' + fieldName,'toolbar=no,location=no,status=no,menubar=no,scrollbars=yes,resizable=yes,width=760,height=600');
}

// function to return a single reference from the popup window back into the widget
function bibrefbrowser_setReference(widget_id, uid, label)
{
    element=document.getElementById(widget_id);
    label_element=document.getElementById(widget_id + '_label');
    element.value=uid;
    label_element.value=label;
}

// function to return a reference from the popup window back into the multivalued widget
function bibrefbrowser_addReference(widget_id, uid, label)
{
    list=document.getElementById(widget_id)
    // check if the item isn't already in the list
    for (var x=0; x < list.length; x++) {
      if (list[x].value == uid) {
        return false;
      }
    }         
    // now add the new item
    theLength=list.length;
    list[theLength] = new Option(label);
    list[theLength].selected='selected';
    list[theLength].value=uid
}

// function to clear the reference field
function bibrefbrowser_clearReference(widget_id)
{
    element=document.getElementById(widget_id);
    label_element=document.getElementById(widget_id + '_label');
    label_element.value = "";
    element.value="";
}

// fonction to remove items from the multivalued reference list.
function bibrefbrowser_removeReference(widget_id)
{
    list=document.getElementById(widget_id)
    for (var x=list.length-1; x >= 0; x--) {
      if (list[x].selected) {
        list[x]=null;
      }
    }
    for (var x=0; x < list.length; x++) {
        list[x].selected='selected';
      }        
}
