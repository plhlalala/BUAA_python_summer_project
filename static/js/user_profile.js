document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('profile-form');
    const avatarInput = document.getElementById('id_avatar');
    const avatarPreview = document.getElementById('avatar-preview');

    avatarInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                avatarPreview.src = e.target.result;
            };
            reader.readAsDataURL(file);
        }
    });

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(form);

        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('个人信息更新成功！');
            } else {
                alert('更新个人信息时发生错误。请重试。');
                console.error(data.errors);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('发生错误。请重试。');
        });
    });
});