import cn from 'classnames'

import styles from './style.module.css'

const Button = ({
                    children,
                    modifier = "style_light-blue",
                    href,
                    clickHandler,
                    className,
                    disabled,
                    type = 'button',
                    isActive,
                    title
                }) => {
    let mod_active = isActive ? "style_dark-blue" : "style_light-blue"
    const classNames = cn(styles.button, className, {
        [styles[`button_${mod_active}`]]: mod_active,
        [styles.button_disabled]: disabled
    });
    if (href) {
        return (
            <a className={classNames} href={href}>
                {children}
            </a>
        );
    }
    return (
        <button
            title={title}
            className={classNames}
            disabled={disabled}
            onClick={(event) => clickHandler && clickHandler(event)}
        >
            {children}
        </button>
    );
};

export default Button;
