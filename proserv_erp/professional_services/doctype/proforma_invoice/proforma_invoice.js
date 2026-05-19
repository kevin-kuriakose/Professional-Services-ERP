frappe.ui.form.on('Proforma Invoice', {
    discount: function(frm) {
        frm.save();
    }
});
