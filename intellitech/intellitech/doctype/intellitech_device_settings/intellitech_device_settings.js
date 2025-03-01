frappe.ui.form.on("Intellitech Device Settings", {
    refresh: function (frm) {
        frm.add_custom_button("Execute", function () {
            frappe.call({
                method: "intellitech.intellitech.api.checksync.process_checkins",
                args: {
                    docname: frm.doc.name
                },
                callback: function (response) {
                    frappe.msgprint(response.message);
                }
            });
        },); 
    }
});
