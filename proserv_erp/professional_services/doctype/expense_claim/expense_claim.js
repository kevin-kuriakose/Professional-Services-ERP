frappe.ui.form.on('Expense Claim', {});

frappe.ui.form.on('Expense Claim Item', {
    amount: function(frm) {
        let total = 0;
        (frm.doc.expenses || []).forEach(row => { total += flt(row.amount); });
        frm.set_value('total_amount', total);
    },
    expenses_remove: function(frm) {
        let total = 0;
        (frm.doc.expenses || []).forEach(row => { total += flt(row.amount); });
        frm.set_value('total_amount', total);
    }
});
