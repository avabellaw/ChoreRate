export default function btnClickMsg(btn, event) {   
    let clickMessage = document.querySelector(btn.dataset.clickMsg);

    if (clickMessage.classList.contains('show')) {
        return;
    }
    
    clickMessage.classList.add('click-msg', 'show');

    let buttonY = btn.getBoundingClientRect().top;
    let clickMsgWidth = clickMessage.offsetWidth;
    let clickMsgHeight = clickMessage.offsetHeight

    clickMessage.style.left = `${event.clientX - clickMsgWidth / 2}px`;
    clickMessage.style.top = `${buttonY - clickMsgHeight}px`;

    document.body.appendChild(clickMessage);

    setTimeout(function() {
        clickMessage.classList.remove('show');
    }, 1400);
}