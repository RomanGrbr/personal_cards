/*import cn from 'classnames'

import styles from './style.module.css'*/
import {LinkComponent} from '../index'
import navigation from '../../configs/navigation'
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faEmpire} from '@fortawesome/free-brands-svg-icons';
import {Nav, Navbar} from "react-bootstrap";

const NavFPK = () => {
    return (
        <Navbar style={{color: "white", width: '100%'}}>
            <Navbar.Brand href="/" style={{
                color: 'white',
                display: 'flex',
                flexDirection: 'row',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '19px',
                marginRight: '24px',
            }}>
                <FontAwesomeIcon icon={faEmpire} size="2x" style={{color: '#e74c3c', margin: '0 14.5px 0 5px'}}/>
                ПАО
            </Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav"/>
            <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="me-auto">
                    {navigation.map((item, index) => {
                        return (
                            <div
                                style={{marginLeft: index > 0 ? '16px' : '0', marginTop: '-1px'}}
                                key={index}>
                                <LinkComponent
                                    key={item.title}
                                    title={item.title}
                                    href={item.href}
                                    help={item.help}
                                />
                            </div>
                        );
                    })}
                </Nav>
            </Navbar.Collapse>
        </Navbar>
    );
};

export default NavFPK;
