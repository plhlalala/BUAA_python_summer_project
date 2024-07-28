document.addEventListener('DOMContentLoaded', function() {
    function init() {
        const form = document.getElementById('profile-form');
        if (form) {
            form.removeEventListener('submit', handleFormSubmit);
            form.addEventListener('submit', handleFormSubmit);
            console.log('Event listener re-bound to form submit.');
        }
    }

    // 调用 init 来绑定事件
    init();

    // 如果页面有AJAX加载或其他动态内容变化导致表单被重新创建或修改，确保重新调用 init
    // 例如，可以在AJAX回调或动态内容加载的回调函数中调用 init()
});

async function handleFormSubmit(e) {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);
    console.log('Attempting to submit form.');

    try {
        const response = await fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            }
        });
        const data = await response.json();
        console.log('Response received:', data);
        if (data.success) {
            alert('个人信息更新成功！');
        } else {
            alert('更新个人信息时发生错误。请重试。');
            console.error('Form errors:', data.errors);
        }
    } catch (error) {
        console.error('Error during form submission:', error);
        alert('发生错误。请重试。');
    }
}
