import React, { useState } from 'react';
import PDFModifier from './PDFModifier';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('pdf'); // 'pdf' or 'todo'

  return (
    <div className="App">
      <header className="App-header">
        <h1>Multi-Purpose Application</h1>
        <nav className="tab-navigation">
          <button 
            className={`tab-button ${activeTab === 'pdf' ? 'active' : ''}`}
            onClick={() => setActiveTab('pdf')}
          >
            PDF Text Modifier
          </button>
          <button 
            className={`tab-button ${activeTab === 'todo' ? 'active' : ''}`}
            onClick={() => setActiveTab('todo')}
          >
            Todo App
          </button>
        </nav>
      </header>

      <main className="App-main">
        {activeTab === 'pdf' ? (
          <PDFModifier />
        ) : (
          <Todos />
        )}
      </main>
    </div>
  );
}

// Todo Component (existing functionality)
class Todos extends React.Component {
    constructor(props) {
        super(props);
        this.state = { todos: [], text: '' };
        this.removeTodo = this.removeTodo.bind(this);
    }

    additionTodo(e) {
        e.preventDefault();
        this.setState({ 
        	todos: [ this.state.text, ...this.state.todos ],
        	text: ''
        });
    }

    deleteTodo(name, i){
        let todos = this.state.todos.slice();
        todos.splice(i, 1);
        this.setState({
            todos
        });
    }

    todoUpdate(e) {
        this.setState({ text: e.target.value})
    }

    render() {
        return(
            <div className="card d-flex main-header">
            <div className="card-body">
                <form className="form-group"onSubmit = {(e) => this.addTodo(e)}>
                    <input className="form-control"
                        placeholder="Add Todo"
                        value={this.state.text}
                        onChange={(e) => {this.updateValue(e)}}
                    />
                    <button className="btn btn-primary" type="submit">Add Todo</button>
                </form>
                <TodoList todos={this.state.todos} removeTodo={this.removeTodo}/>
            </div>
            </div>
        );
    }
}

class TodoList extends React.Component {

    deleteItem(item, i) {
        this.props.removeTodo(item, i);
    }

    render() {
        return(
            <ul>
                { this.props.todos.map((todo,i) => {
                    return <li onClick={() => { this.deleteItem(todo, i)}} key={i}>{ todo }</li>
                })}
            </ul>
        );
    }
}

export default App;
