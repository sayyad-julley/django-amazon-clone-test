# Bulk Product Selection Feature

## Overview
The product list page now includes a "Select All" checkbox functionality to enable bulk selection of products.

## Implementation Details
- A "Select All" checkbox is added to the bulk actions section
- Individual product checkboxes are available for each product
- JavaScript function `toggleAllProducts()` handles the select/deselect logic

## Functionality
- Clicking the "Select All" checkbox checks/unchecks all product checkboxes
- Supports bulk actions like delete on selected products

## Location
- Template: `DjangoEcommerceApp/templates/admin_templates/product_list.html`