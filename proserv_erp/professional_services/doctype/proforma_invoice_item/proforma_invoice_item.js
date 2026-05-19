frappe.ui.form.on('Proforma Invoice Item', {
    hours_or_qty: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        frappe.model.set_value(cdt, cdn, 'amount', flt(row.hours_or_qty) * flt(row.rate));
        frm.refresh_field('line_items');
    },
    rate: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        frappe.model.set_value(cdt, cdn, 'amount', flt(row.hours_or_qty) * flt(row.rate));
        frm.refresh_field('line_items');
    }
});
