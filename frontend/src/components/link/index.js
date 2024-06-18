import styles from './style.module.css'

const MyLinkComponent = ({href, children}) => {
    return <a href={href} className={href=='/fpk' ? styles.nav__link_active : styles.nav__link}>{children}</a>
}

const LinkComponent = ({href, title, help}) => {

    return (
        <div title={help}>
            <MyLinkComponent href={href}>{title}</MyLinkComponent>
        </div>

    );
};

export default LinkComponent;
