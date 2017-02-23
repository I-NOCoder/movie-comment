import React, {Component} from 'react';
import {observer} from 'mobx-react';
//import DevTools from 'mobx-react-devtools';
import {List, ListItem} from 'material-ui/List';
import CircularProgress from 'material-ui/CircularProgress';
import FloatingActionButton from 'material-ui/FloatingActionButton';
import NavigationRefresh from 'material-ui/svg-icons/navigation/refresh';
import Divider from 'material-ui/Divider';
import Subheader from 'material-ui/Subheader';
import Avatar from 'material-ui/Avatar';
import {darkBlack, grey400} from 'material-ui/styles/colors';
import withWidth from 'material-ui/utils/withWidth';

import {MEDIUMWIDTH} from './utils';


function getBodyHeight() {
  let height;
  if ( document.body && ( document.body.clientWidth || document.body.clientHeight ) ) {
    height = document.body.clientHeight;
  } else if( document.documentElement && ( document.documentElement.clientWidth || document.documentElement.clientHeight ) ) {
    //IE 6+ in 'standards compliant mode'
    height = document.documentElement.clientHeight;
  } else if( typeof( window.innerWidth ) == 'number' ) {
    height = window.innerHeight;
  }
  return height
}

class Comment extends Component {

  render() {
    const {user, movie, content, like_count} = this.props.comment;
    return (
      <div>
        <ListItem
          leftAvatar={<Avatar src={user.avatar} />}
          primaryText={<a href={movie.url}>{movie.name} 
			<span style={{color: grey400}} >豆瓣评分</span>
			<span style={{color: darkBlack}}>{movie.mark}</span></a> }
          secondaryText={
            <p>
              <span style={{color: darkBlack}}>{user.name}</span> --
                          [{like_count}]{content}
            </p>
                        }
          secondaryTextLines={2}
        />
        <Divider inset={true} />
      </div>
    )
  }
}


@observer
class CommentList extends Component {

  static defaultProps = {
    pcThreshold: 450,
    mobileThreshold: 650,
    threshold: 450,
    perPage: 20
  }

  componentDidMount () {
    this.pending = false;
    this.props.commentStore.loadComments(this.props.commentStore.orderBy, 0, this.props.perPage)
    this.attachScrollListener();
  }

  componentWillMount () {
    let threshold, height;
    if (screen.width > MEDIUMWIDTH) {
      threshold = this.props.pcThreshold;
      height = window.innerHeight;
    } else {
      threshold = this.props.mobileThreshold;
      height = screen.height;
    }
    this.threshold = threshold;
    this.height = height;
  }

  scrollListener = () => {

    var scrollTop = (window.pageYOffset !== undefined) ? window.pageYOffset : (document.documentElement || document.body.parentNode || document.body).scrollTop;
    let threshold = this.threshold;
    if (screen.width < MEDIUMWIDTH) {
      threshold = threshold * (this.props.commentStore.pageLoaded / this.props.perPage + 1 );
    }
    if (getBodyHeight() - scrollTop - this.height < Number(threshold) && !this.props.commentStore.useSearch) {
       if (this.pending) {
         return
       }
      this.pending = true;
      this.props.commentStore.loadComments(this.props.commentStore.orderBy, this.props.commentStore.pageLoaded += this.props.perPage, this.props.perPage, () =>(
        this.pending = false
      ));
    }
  }

  attachScrollListener () {
    if (!this.props.commentStore.hasMore) {
      return;
    }
    window.addEventListener('scroll', this.scrollListener, false);
    window.addEventListener('resize', this.scrollListener, false);
    this.scrollListener();
  }

  detachScrollListener () {
    window.removeEventListener('scroll', this.scrollListener, false);
    window.removeEventListener('resize', this.scrollListener, false);
  }

  componentWillUnmount () {
    this.detachScrollListener();
  }

  render() {
    const style = {
      textAlign: 'center',
      height: 600
    };
    let buttonStyle = {
      margin: 30,
      float: 'right',
      cursor: 'pointer'
    };

    const {comments, pending} = this.props.commentStore;
    let promotion = '';

    if (pending) {
      promotion = <div style={style}><CircularProgress size={1.5}/></div>
    } else if (!comments.length) {
      buttonStyle = Object.assign(buttonStyle, {'float': 'none'});
      promotion = <div style={style}><p>没有搜到评论哎😌  点下边刷新按钮看看</p>
         <FloatingActionButton onClick={this.onReset} style={buttonStyle}>
           <NavigationRefresh/>
         </FloatingActionButton>
      </div>
    }
    let debugPanel;
	/*
    if (__DEV__) {
      debugPanel = (
        <DevTools />
      );
    }*/
    return (
      <div>
        {promotion}
        <div className="comment-list">
          <List>
            <Subheader>{'按评论数'}</Subheader>
            {
              comments.map((comment, index) => {
                  return <Comment comment={comment} key={index}/>
              })
            }
          </List>
        </div>
        {debugPanel}
      </div>
    )
  }

  onReset = () => {
    this.props.commentStore.resetComments(this.props.commentStore.orderBy);
  }
}

export default withWidth()(CommentList);
