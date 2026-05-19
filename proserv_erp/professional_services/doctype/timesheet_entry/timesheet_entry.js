frappe.ui.form.on('Timesheet Entry', {
    hours: function(frm) {
        frm.set_value('billable_amount', flt(frm.doc.hours) * flt(frm.doc.billing_rate));
    },
    billing_rate: function(frm) {
        frm.set_value('billable_amount', flt(frm.doc.hours) * flt(frm.doc.billing_rate));
    },
    billing_type: function(frm) {
        if (frm.doc.billing_type !== 'Billable') {
            frm.set_value('billable_amount', 0);
        }
    }
});
