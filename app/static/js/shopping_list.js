document.addEventListener("DOMContentLoaded", () => {

    document
        .querySelectorAll(".shopping-quantity-input, .shopping-unit-input, .shopping-comment-input")
        .forEach(field => {

            field.addEventListener("blur", () => {

                saveShoppingItem(field.dataset.itemId);

            });

        });

});


async function saveShoppingItem(itemId) {

    const quantityInput = document.querySelector(
        `.shopping-quantity-input[data-item-id="${itemId}"]`
    );

    const unitInput = document.querySelector(
        `.shopping-unit-input[data-item-id="${itemId}"]`
    );

    const noteInput = document.querySelector(
        `.shopping-comment-input[data-item-id="${itemId}"]`
    );

    const formData = new FormData();

    formData.append("quantity", quantityInput.value);
    formData.append("unit", unitInput.value);
    formData.append("note", noteInput.value);

    const response = await fetch(
        `/shopping-list-items/${itemId}/update`,
        {
            method: "POST",
            body: formData
        }
    );

    const data = await response.json();

    console.log(data);
}
