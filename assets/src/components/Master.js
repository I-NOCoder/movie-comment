import React, {Component, PropTypes} from 'react';
import Title from 'react-title-component';
import AppBar from 'material-ui/AppBar';
import IconButton from 'material-ui/IconButton';
import spacing from 'material-ui/styles/spacing';
import getMuiTheme from 'material-ui/styles/getMuiTheme';
import {darkWhite, lightWhite, grey900} from 'material-ui/styles/colors';
import FullWidthSection from './FullWidthSection';
import withWidth, {MEDIUM, LARGE} from 'material-ui/utils/withWidth';

class Master extends Component {
  static propTypes = {
    children: PropTypes.node,
    location: PropTypes.object,
    width: PropTypes.number.isRequired,
  };

  static contextTypes = {
    router: PropTypes.object.isRequired,
  };

  static childContextTypes = {
    muiTheme: PropTypes.object,
  };

  state = {
    navDrawerOpen: false,
  };

  getChildContext() {
    return {
      muiTheme: this.state.muiTheme,
    };
  }

  componentWillMount() {
    this.setState({
      muiTheme: getMuiTheme(),
    });
  }

  componentWillReceiveProps(nextProps, nextContext) {
    const newMuiTheme = nextContext.muiTheme ? nextContext.muiTheme : this.state.muiTheme;
    this.setState({
      muiTheme: newMuiTheme,
    });
  }

  getStyles() {
    const styles = {
      appBar: {
        position: 'fixed',
        zIndex: this.state.muiTheme.zIndex.appBar + 1,
        top: 0,
      },
      root: {
        paddingTop: spacing.desktopKeylineIncrement,
        minHeight: 400,
      },
      content: {
        margin: spacing.desktopGutter,
      },
      contentWhenMedium: {
        margin: `${spacing.desktopGutter * 2}px ${spacing.desktopGutter * 3}px`,
      },
      footer: {
        backgroundColor: grey900,
        textAlign: 'center'
      },
      a: {
        color: darkWhite,
      },
      p: {
        margin: '0 auto',
        padding: 0,
        color: lightWhite,
        maxWidth: 356,
      },
      netease: {
        display: 'flex',
        alignItems: 'flex-start',
        justifyContent: 'center',
        padding: 0,
        color: lightWhite,
        lineHight: '25px',
        fontSize: 15,
      },
      neteaseLogo: {
        margin: '0 3px',
      },
      iconButton: {
        color: darkWhite,
      },
    };

    if (this.props.width === MEDIUM || this.props.width === LARGE) {
      styles.content = Object.assign(styles.content, styles.contentWhenMedium);
    }

    return styles;
  }


  handleChangeMuiTheme = (muiTheme) => {
    this.setState({
      muiTheme: muiTheme,
    });
  };

  render() {
    const {
      children,
    } = this.props;

  
    const {
      prepareStyles,
    } = this.state.muiTheme;

    const styles = this.getStyles();
    const title = '';

    return (
      <div>
        <Title render="豆瓣电影评论" />
        <AppBar
          title={title}
          zDepth={0}
          iconElementRight={
            <IconButton
              iconClassName="muidocs-icon-custom-github"
              href="https://github.com/I-NOCoder/douban-movie-commentbox"
            />
          }
          style={styles.appBar}
          
        />
        {title !== '' ?
          <div style={prepareStyles(styles.root)}>
            <div style={prepareStyles(styles.content)}>
              {React.cloneElement(children, {
                onChangeMuiTheme: this.handleChangeMuiTheme,
              })}
            </div>
          </div> :
          children
        }
    
        <FullWidthSection style={styles.footer}>
          <IconButton
            iconStyle={styles.iconButton}
            iconClassName="muidocs-icon-custom-github"
            href="https://github.com/I-NOCoder/commentbox"
          />
          <p style={prepareStyles(styles.netease)}>
            {'Thank you to '}
            <a href="https://movie.douban.com/" style={prepareStyles(styles.neteaseLogo)} target="_blank">
              豆瓣电影
            </a>
            {' for providing comments.'}
          </p>
        </FullWidthSection>
      </div>
    );
  }
}

export default withWidth()(Master);
