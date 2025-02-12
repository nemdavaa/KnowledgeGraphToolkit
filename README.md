# KnowledgeGraphToolkit

## Overview
The **KnowledgeGraphToolkit** is a modular and extensible framework designed to facilitate the construction, querying, and visualisation of knowledge graphs using GraphDB. This project forms part of a bachelor's thesis focused on exploring efficient techniques for integrating and analysing heterogeneous data sources.

## Key Features
- **Graph Construction:** Build complex knowledge graphs with diverse relationships between data entities.
- **Querying Capabilities:** Perform semantic queries using SPARQL, enabling advanced pattern discovery.
- **Extensibility:** Support for plugin development to extend the framework's functionality.
- **Visualisation:** Tools for rendering and navigating graph data structures.

## Motivation
Heterogeneous data integration poses a significant challenge for cloud-native and large-scale application systems. Traditional relational and document-oriented databases often struggle to capture intricate relationships between dynamic data elements. Knowledge graphs offer a powerful alternative by representing entities and their relationships as nodes and edges, facilitating inference and advanced semantic querying.

### Real-World Applications
Knowledge graphs are widely adopted by major technology companies for their ability to unlock insights from interconnected data:
- **Google Knowledge Graph:** Enhances search capabilities by connecting information about people, places, and concepts. [(Source)](https://www.blog.google/products/search/introducing-knowledge-graph-things-not/)  
- **LinkedIn Economic Graph:** Maps workforce relationships, enabling insights into market dynamics. [(Source)](https://engineering.linkedin.com/blog/2016/10/exploring-the-economic-graph)  
- **Amazon Product Graph:** Analyses customer behaviour and product relationships for optimised recommendations. [(Source)](https://www.aboutamazon.com/news/innovation-at-amazon/how-amazon-uses-machine-learning-to-better-understand-products)  

## Why GraphDB?
This project utilises **GraphDB** due to its:
- Compliance with W3C standards
- Efficient SPARQL query engine
- Robust support for RDF data modelling

While alternatives like Neo4j and Blazegraph exist, GraphDB was chosen for its strong focus on semantic data integration and high-performance querying.

## Running GraphDB with Docker

This project integrates with [GraphDB](https://www.ontotext.com/products/graphdb/). You can use Docker to easily run GraphDB locally.

### Using Docker Compose

1. Clone the repository:
    ```bash
    git clone https://github.com/nemdavaa00/KnowledgeGraphToolkit.git
    cd KnowledgeGraphToolkit
    ```

2. Navigate to the `docker/` directory:
    ```bash
    cd docker
    ```

3. Run Docker Compose to start GraphDB:
    ```bash
    docker-compose up
    ```

4. Once GraphDB is running, open [http://localhost:7200](http://localhost:7200) in your browser to access the GraphDB Workbench.

### Manual GraphDB Setup

Alternatively, you can manually install GraphDB. Follow the instructions provided by [GraphDB's official documentation](https://www.ontotext.com/products/graphdb/download/).

## Project Structure
- `core/`: Contains the main framework components.
- `plugins/`: Custom extensions and additional modules.
- `visualisation/`: Tools for graph visualisation.
- `docs/`: Documentation for framework usage and plugin development.

## Usage
### Installation
Clone the repository and set up the required environment:
```bash
$ git clone https://github.com/nemdavaa00/KnowledgeGraphToolkit.git
$ cd KnowledgeGraphToolkit
```

### Running the Framework
```bash
$ python main.py
```

### Querying Graphs
Example SPARQL query usage:
```sparql
SELECT ?subject ?predicate ?object
WHERE {
  ?subject ?predicate ?object.
}
```

### Plugin Development
To develop a custom plugin, follow these steps:
1. Create a new Python module in the `plugins/` directory.
2. Implement the required interfaces defined in `core/plugin_base.py`.
3. Register the plugin in the configuration file.

## Future Work
- Integration with machine learning models for graph-based AI insights
- Mathematical analysis using techniques like Markov chains to assess system dependencies
- Enhanced visualisation and interaction features

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request for review.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgements
Special thanks to the academic supervisors and contributors who supported the development of this project.
