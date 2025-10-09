"use client";

import { useEffect, useRef, useState } from "react";
import * as d3 from "d3";

interface Node {
  id: string;
  label: string;
  category: string;
  traders: number;
  volume: number;
}

interface Edge {
  source: string;
  target: string;
  weight: number;
}

interface NetworkData {
  nodes: Node[];
  edges: Edge[];
}

export default function NetworkGraph() {
  const svgRef = useRef<SVGSVGElement>(null);
  const [data, setData] = useState<NetworkData | null>(null);
  const [selectedCategory, setSelectedCategory] = useState<string>("all");
  const [selectedNodeInfo, setSelectedNodeInfo] = useState<Node | null>(null);
  const [searchQuery, setSearchQuery] = useState<string>("");
  const selectedNodeRef = useRef<string | null>(null);
  const hoveredEdgeRef = useRef<string | null>(null);
  const edgeLabelsRef = useRef<any>(null);
  const nodeLabelsRef = useRef<any>(null);
  const nodesRef = useRef<any>(null);
  const edgesRef = useRef<any>(null);
  const graphEdgesRef = useRef<any[]>([]);

  useEffect(() => {
    fetch("/network.json")
      .then((res) => res.json())
      .then((data: NetworkData) => setData(data));
  }, []);

  useEffect(() => {
    if (!data || !svgRef.current) return;

    const svg = d3.select(svgRef.current);
    svg.selectAll("*").remove();

    const width = 1200;
    const height = 800;

    svg.attr("viewBox", [0, 0, width, height]);

    const g = svg.append("g");

    // Zoom behavior - allow more zoom out
    const zoom = d3.zoom<SVGSVGElement, unknown>()
      .scaleExtent([0.1, 4])
      .on("zoom", (event) => {
        g.attr("transform", event.transform);
      });

    svg.call(zoom as any);

    // Filter nodes by category and search
    let filteredNodes = selectedCategory === "all"
      ? data.nodes
      : data.nodes.filter((n) => n.category === selectedCategory);
    
    // Apply search filter
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      filteredNodes = filteredNodes.filter((n) => 
        n.label.toLowerCase().includes(query)
      );
    }
    
    const nodeIds = new Set(filteredNodes.map((n) => n.id));
    const filteredEdges = data.edges.filter(
      (e) => nodeIds.has(e.source) && nodeIds.has(e.target)
    );

    // Category colors
    const categories = Array.from(new Set(data.nodes.map((n) => n.category)));
    const colorScale = d3.scaleOrdinal(d3.schemeCategory10).domain(categories);

    // Create d3-compatible nodes with initial positions near center
    const graphNodes = filteredNodes.map(n => ({
      ...n,
      x: width / 2 + (Math.random() - 0.5) * 400,
      y: height / 2 + (Math.random() - 0.5) * 400
    }));
    const graphEdges = filteredEdges.map(e => ({...e}));

    // Simulation - balanced clustering with readable labels
    const simulation = d3
      .forceSimulation(graphNodes as any)
      .force(
        "link",
        d3
          .forceLink(graphEdges)
          .id((d: any) => d.id)
          .distance(120)
          .strength(0.3)
      )
      .force("charge", d3.forceManyBody().strength(-250))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collision", d3.forceCollide().radius(35))
      .force("x", d3.forceX(width / 2).strength(0.05))
      .force("y", d3.forceY(height / 2).strength(0.05))
      .alphaDecay(0.02)
      .velocityDecay(0.4);

    // Links - much lighter for readability with 633 connections
    const link = g
      .append("g")
      .selectAll("line")
      .data(graphEdges)
      .join("line")
      .attr("stroke", "#6b7280")
      .attr("stroke-opacity", 0.15) // Very light default
      .attr("stroke-width", 0.5) // Very thin default
      .style("cursor", "pointer")
      .on("mouseenter", function(event, d: any) {
        hoveredEdgeRef.current = `${d.source.id}-${d.target.id}`;
        d3.select(this)
          .attr("stroke", "#60a5fa")
          .attr("stroke-opacity", 0.9)
          .attr("stroke-width", 2.5);
        
        if (edgeLabelsRef.current) {
          edgeLabelsRef.current
            .filter((e: any) => `${e.source.id}-${e.target.id}` === hoveredEdgeRef.current)
            .style("opacity", 1);
        }
      })
      .on("mouseleave", function(event, d: any) {
        hoveredEdgeRef.current = null;
        d3.select(this)
          .attr("stroke", "#6b7280")
          .attr("stroke-opacity", 0.15)
          .attr("stroke-width", 0.5);
        
        if (edgeLabelsRef.current) {
          edgeLabelsRef.current.style("opacity", 0);
        }
      });
    
    // Edge labels
    const edgeLabel = g
      .append("g")
      .selectAll("text")
      .data(graphEdges)
      .join("text")
      .attr("font-size", 11)
      .attr("fill", "#60a5fa")
      .attr("font-weight", "bold")
      .attr("text-anchor", "middle")
      .attr("pointer-events", "none")
      .text((d) => `${d.weight.toFixed(1)}%`)
      .style("opacity", 0);
    
    edgeLabelsRef.current = edgeLabel;

    // Store graph edges for external access
    graphEdgesRef.current = graphEdges;

    // Nodes
    const node = g
      .append("g")
      .selectAll("circle")
      .data(graphNodes)
      .join("circle")
      .attr("r", (d) => Math.sqrt(d.volume) / 5000 + 6)
      .attr("fill", (d) => colorScale(d.category))
      .attr("stroke", "#fff")
      .attr("stroke-width", 1.5)
      .style("cursor", "pointer")
      .on("click", function(event, d: any) {
        event.stopPropagation();
        
        // Open Polymarket URL on Ctrl/Cmd+Click
        if (event.ctrlKey || event.metaKey) {
          window.open(`https://polymarket.com/event/${d.id}`, '_blank');
          return;
        }
        
        selectedNodeRef.current = d.id;
        setSelectedNodeInfo({...d});
        
        // Find connected node IDs
        const connectedIds = new Set<string>();
        connectedIds.add(d.id);
        graphEdges.forEach((edge: any) => {
          if (edge.source.id === d.id) connectedIds.add(edge.target.id);
          if (edge.target.id === d.id) connectedIds.add(edge.source.id);
        });
        
        // Highlight selected + connected nodes
        d3.selectAll("circle")
          .attr("stroke-width", 1.5)
          .attr("opacity", (n: any) => connectedIds.has(n.id) ? 1 : 0.3);
        d3.select(this).attr("stroke-width", 4).attr("opacity", 1);
        
        // Highlight connected edges
        d3.selectAll("line")
          .attr("stroke-opacity", (e: any) => 
            (e.source.id === d.id || e.target.id === d.id) ? 0.6 : 0.05
          )
          .attr("stroke-width", (e: any) => 
            (e.source.id === d.id || e.target.id === d.id) ? 1.5 : 0.5
          );
        
        if (nodeLabelsRef.current) {
          nodeLabelsRef.current
            .style("opacity", (n: any) => 
              n.traders > 3000 || connectedIds.has(n.id) ? 1 : 0
            );
        }
      })
      .call(
        d3.drag<any, any>()
          .on("start", (event, d: any) => {
            if (!event.active) simulation.alphaTarget(0.1).restart();
            d.fx = d.x;
            d.fy = d.y;
          })
          .on("drag", (event, d: any) => {
            d.fx = event.x;
            d.fy = event.y;
          })
          .on("end", (event, d: any) => {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
          })
      );

    // Labels (all nodes, but only show for large or selected)
    const label = g
      .append("g")
      .selectAll("text")
      .data(graphNodes)
      .join("text")
      .text((d) => d.label.substring(0, 25))
      .attr("font-size", 11)
      .attr("fill", "#e5e7eb")
      .attr("font-weight", "500")
      .attr("text-anchor", "middle")
      .attr("dy", -18)
      .attr("pointer-events", "none")
      .style("opacity", (d) => d.traders > 3000 ? 1 : 0);
    
    nodeLabelsRef.current = label;
    nodesRef.current = node;
    edgesRef.current = link;

    // Function to highlight a node from outside D3
    const highlightNode = (nodeId: string) => {
      const nodeData = graphNodes.find((n: any) => n.id === nodeId);
      if (!nodeData) return;

      selectedNodeRef.current = nodeId;
      setSelectedNodeInfo(nodeData);

      // Find connected node IDs
      const connectedIds = new Set<string>();
      connectedIds.add(nodeId);
      graphEdgesRef.current.forEach((edge: any) => {
        if (edge.source.id === nodeId) connectedIds.add(edge.target.id);
        if (edge.target.id === nodeId) connectedIds.add(edge.source.id);
      });

      // Highlight nodes
      node
        .attr("stroke-width", 1.5)
        .attr("opacity", (n: any) => connectedIds.has(n.id) ? 1 : 0.3);
      
      node.filter((n: any) => n.id === nodeId)
        .attr("stroke-width", 4)
        .attr("opacity", 1);

      // Highlight edges
      link
        .attr("stroke-opacity", (e: any) => 
          (e.source.id === nodeId || e.target.id === nodeId) ? 0.6 : 0.05
        )
        .attr("stroke-width", (e: any) => 
          (e.source.id === nodeId || e.target.id === nodeId) ? 1.5 : 0.5
        );

      // Highlight labels
      if (nodeLabelsRef.current) {
        nodeLabelsRef.current
          .style("opacity", (n: any) => 
            n.traders > 3000 || connectedIds.has(n.id) ? 1 : 0
          );
      }
    };

    // Store highlight function in window for external access
    (window as any).highlightNode = highlightNode;

    // Tooltips
    node.append("title").text(
      (d) =>
        `${d.label}\n${d.category}\n${d.traders.toLocaleString()} traders\n$${(
          d.volume / 1e6
        ).toFixed(1)}M volume`
    );

    simulation.on("tick", () => {
      link
        .attr("x1", (d: any) => d.source.x)
        .attr("y1", (d: any) => d.source.y)
        .attr("x2", (d: any) => d.target.x)
        .attr("y2", (d: any) => d.target.y);
      
      edgeLabel
        .attr("x", (d: any) => (d.source.x + d.target.x) / 2)
        .attr("y", (d: any) => (d.source.y + d.target.y) / 2);

      node.attr("cx", (d: any) => d.x).attr("cy", (d: any) => d.y);

      label
        .attr("x", (d: any) => d.x)
        .attr("y", (d: any) => d.y);
    });
    
    // Click background to deselect
    svg.on("click", () => {
      selectedNodeRef.current = null;
      setSelectedNodeInfo(null);
      d3.selectAll("circle").attr("stroke-width", 1.5).attr("opacity", 1);
      d3.selectAll("line").attr("stroke-opacity", 0.15).attr("stroke-width", 0.5);
      
      if (nodeLabelsRef.current) {
        nodeLabelsRef.current
          .style("opacity", (d: any) => d.traders > 3000 ? 1 : 0);
      }
    });

    return () => {
      simulation.stop();
    };
  }, [data, selectedCategory, searchQuery]);

  if (!data) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-gray-500">Loading network...</div>
      </div>
    );
  }

  const categories = ["all", ...Array.from(new Set(data.nodes.map((n) => n.category)))];
  const categoryColors = d3.scaleOrdinal(d3.schemeCategory10).domain(categories.filter(c => c !== "all"));

  return (
    <div className="space-y-4">
      {/* Stats Overview */}
      <div className="grid grid-cols-4 gap-4">
        <div className="bg-gray-800 p-3 rounded border border-gray-700">
          <div className="text-2xl font-bold text-white">{data.nodes.length}</div>
          <div className="text-xs text-gray-400">Events</div>
        </div>
        <div className="bg-gray-800 p-3 rounded border border-gray-700">
          <div className="text-2xl font-bold text-white">{data.edges.length}</div>
          <div className="text-xs text-gray-400">Connections</div>
        </div>
        <div className="bg-gray-800 p-3 rounded border border-gray-700">
          <div className="text-2xl font-bold text-white">${(data.nodes.reduce((sum, n) => sum + n.volume, 0) / 1e9).toFixed(1)}B</div>
          <div className="text-xs text-gray-400">Total Volume</div>
        </div>
        <div className="bg-gray-800 p-3 rounded border border-gray-700">
          <div className="text-2xl font-bold text-white">{(data.edges.reduce((sum, e) => sum + e.weight, 0) / data.edges.length).toFixed(1)}%</div>
          <div className="text-xs text-gray-400">Avg Overlap</div>
        </div>
      </div>

      {/* Search Bar */}
      <div className="mb-4">
        <input
          type="text"
          placeholder="Search events..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
        />
      </div>

      {/* Category Filters */}
      <div className="flex gap-2 flex-wrap">
        {categories.slice(0, 15).map((cat) => (
          <button
            key={cat}
            onClick={() => setSelectedCategory(cat)}
            className={`px-3 py-1 rounded text-sm flex items-center gap-2 ${
              selectedCategory === cat
                ? "bg-blue-600 text-white"
                : "bg-gray-800 text-gray-400 hover:bg-gray-700"
            }`}
          >
            {cat !== "all" && (
              <span 
                className="w-3 h-3 rounded-full" 
                style={{ backgroundColor: categoryColors(cat) as string }}
              />
            )}
            {cat === "all" ? "All" : cat}
          </button>
        ))}
      </div>

      <div className="overflow-hidden">
        <svg ref={svgRef} className="w-full cursor-grab active:cursor-grabbing" style={{ height: "800px" }} />
      </div>
      
      {selectedNodeInfo && (
        <div className="mt-4 space-y-4">
          <div className="p-4 bg-gray-800 rounded-lg border border-gray-700">
            <div className="flex items-start justify-between mb-2">
              <h3 className="font-semibold text-white text-lg flex-1">
                {selectedNodeInfo.label}
              </h3>
              <span 
                className="w-4 h-4 rounded-full flex-shrink-0 mt-1" 
                style={{ backgroundColor: categoryColors(selectedNodeInfo.category) as string }}
              />
            </div>
            <a 
              href={`https://polymarket.com/event/${selectedNodeInfo.id}`}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-400 hover:text-blue-300 text-sm flex items-center gap-1 mb-3"
            >
              View on Polymarket
              <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
              </svg>
            </a>
            <div className="grid grid-cols-3 gap-4 text-sm">
              <div>
                <div className="text-gray-500 text-xs">Category</div>
                <div className="text-white font-medium">{selectedNodeInfo.category}</div>
              </div>
              <div>
                <div className="text-gray-500 text-xs">Traders</div>
                <div className="text-white font-medium">{selectedNodeInfo.traders.toLocaleString()}</div>
              </div>
              <div>
                <div className="text-gray-500 text-xs">Volume</div>
                <div className="text-white font-medium">${(selectedNodeInfo.volume / 1e6).toFixed(2)}M</div>
              </div>
            </div>
          </div>

          {/* Connections Table */}
          <div className="p-4 bg-gray-800 rounded-lg border border-gray-700">
            <h4 className="font-semibold text-white mb-3">
              Connected Events ({data.edges.filter((e: any) => 
                e.source === selectedNodeInfo.id || e.target === selectedNodeInfo.id
              ).length})
            </h4>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-gray-700">
                    <th className="text-left py-2 text-gray-400 font-medium">Event</th>
                    <th className="text-left py-2 text-gray-400 font-medium">Category</th>
                    <th className="text-right py-2 text-gray-400 font-medium">Overlap</th>
                    <th className="text-right py-2 text-gray-400 font-medium">Volume</th>
                  </tr>
                </thead>
                <tbody>
                  {data.edges
                    .filter((e: any) => e.source === selectedNodeInfo.id || e.target === selectedNodeInfo.id)
                    .sort((a: any, b: any) => b.weight - a.weight)
                    .map((edge: any, idx: number) => {
                      const connectedId = edge.source === selectedNodeInfo.id ? edge.target : edge.source;
                      const connectedNode = data.nodes.find((n: any) => n.id === connectedId);
                      if (!connectedNode) return null;
                      const isTopRecommendation = idx === 0;
                      return (
                        <tr 
                          key={idx} 
                          className={`border-b border-gray-700/50 hover:bg-gray-700/30 ${
                            isTopRecommendation ? 'bg-blue-900/20 border-blue-500/30' : ''
                          }`}
                        >
                          <td className="py-2 text-white">
                            {connectedNode.label}
                            {isTopRecommendation && (
                              <span className="ml-2 text-xs bg-blue-500 text-white px-2 py-0.5 rounded font-medium">
                                Highest overlap
                              </span>
                            )}
                          </td>
                          <td className="py-2 text-gray-400 text-xs">{connectedNode.category}</td>
                          <td className="py-2 text-right">
                            <span className={`font-medium ${isTopRecommendation ? 'text-blue-300' : 'text-blue-400'}`}>
                              {edge.weight.toFixed(1)}%
                            </span>
                          </td>
                          <td className="py-2 text-right text-gray-400">${(connectedNode.volume / 1e6).toFixed(1)}M</td>
                        </tr>
                      );
                    })}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
      
      <div className="text-xs text-gray-500 text-center mt-2">
        Click node to select • Cmd/Ctrl+Click to open on Polymarket • Hover edge to see % • Drag to pan • Scroll to zoom
      </div>

      {/* Analytics Section */}
      <div className="mt-8 pt-6 border-t border-gray-800">
        <h3 className="text-lg font-semibold text-white mb-4">Network Insights</h3>
        
        <div className="grid grid-cols-2 gap-4">
          {/* Top Connected Events */}
          <div className="bg-gray-800 p-4 rounded-lg border border-gray-700">
            <h4 className="text-sm font-medium text-gray-400 mb-3">Most Connected Events</h4>
            <div className="space-y-2 max-h-64 overflow-y-auto">
              {(() => {
                // Filter nodes by category first
                const filteredNodes = selectedCategory === "all" 
                  ? data.nodes 
                  : data.nodes.filter((n: any) => n.category === selectedCategory);
                const nodeIds = new Set(filteredNodes.map((n: any) => n.id));
                
                // Filter edges to only include filtered nodes
                const filteredEdges = data.edges.filter((e: any) => 
                  nodeIds.has(e.source) && nodeIds.has(e.target)
                );
                
                const connectionCounts: { [key: string]: number } = {};
                filteredEdges.forEach((edge: any) => {
                  connectionCounts[edge.source] = (connectionCounts[edge.source] || 0) + 1;
                  connectionCounts[edge.target] = (connectionCounts[edge.target] || 0) + 1;
                });
                
                return Object.entries(connectionCounts)
                  .sort((a, b) => b[1] - a[1])
                  .map(([id, count]) => {
                    const node = data.nodes.find((n: any) => n.id === id);
                    return node ? (
                      <div key={id} className="flex justify-between items-center text-sm">
                        <span 
                          className="text-white truncate flex-1 cursor-pointer hover:text-blue-400"
                          onClick={() => {
                            if ((window as any).highlightNode) {
                              (window as any).highlightNode(id);
                            }
                          }}
                        >
                          {node.label.substring(0, 35)}...
                        </span>
                        <span className="text-blue-400 font-medium ml-2">{count}</span>
                      </div>
                    ) : null;
                  });
              })()}
            </div>
          </div>

          {/* Strongest Connections */}
          <div className="bg-gray-800 p-4 rounded-lg border border-gray-700">
            <h4 className="text-sm font-medium text-gray-400 mb-3">Strongest Overlaps</h4>
            <div className="space-y-2 max-h-64 overflow-y-auto">
              {(() => {
                // Filter nodes by category first
                const filteredNodes = selectedCategory === "all" 
                  ? data.nodes 
                  : data.nodes.filter((n: any) => n.category === selectedCategory);
                const nodeIds = new Set(filteredNodes.map((n: any) => n.id));
                
                // Filter edges to only include filtered nodes
                return data.edges
                  .filter((e: any) => nodeIds.has(e.source) && nodeIds.has(e.target))
                  .sort((a: any, b: any) => b.weight - a.weight)
                  .map((edge: any, idx: number) => {
                    const sourceNode = data.nodes.find((n: any) => n.id === edge.source);
                    const targetNode = data.nodes.find((n: any) => n.id === edge.target);
                    return (
                      <div key={idx} className="text-sm">
                        <div className="flex justify-between items-center gap-1">
                          <div className="flex items-center gap-1 flex-1 min-w-0">
                            <span 
                              className="text-white text-xs truncate cursor-pointer hover:text-blue-400"
                              onClick={() => {
                                if ((window as any).highlightNode) {
                                  (window as any).highlightNode(edge.source);
                                }
                              }}
                            >
                              {sourceNode?.label.substring(0, 15)}...
                            </span>
                            <span className="text-gray-500 text-xs">↔</span>
                            <span 
                              className="text-white text-xs truncate cursor-pointer hover:text-blue-400"
                              onClick={() => {
                                if ((window as any).highlightNode) {
                                  (window as any).highlightNode(edge.target);
                                }
                              }}
                            >
                              {targetNode?.label.substring(0, 15)}...
                            </span>
                          </div>
                          <span className="text-blue-400 font-medium text-xs ml-2">{edge.weight.toFixed(1)}%</span>
                        </div>
                      </div>
                    );
                  });
              })()}
            </div>
          </div>

          {/* Category Breakdown */}
          <div className="bg-gray-800 p-4 rounded-lg border border-gray-700">
            <h4 className="text-sm font-medium text-gray-400 mb-3">Top Categories by Volume</h4>
            <div className="space-y-2">
              {(() => {
                const categoryVolumes: { [key: string]: number } = {};
                data.nodes.forEach((node: any) => {
                  categoryVolumes[node.category] = (categoryVolumes[node.category] || 0) + node.volume;
                });
                return Object.entries(categoryVolumes)
                  .sort((a, b) => b[1] - a[1])
                  .slice(0, 5)
                  .map(([cat, vol]) => (
                    <div key={cat} className="flex justify-between items-center text-sm">
                      <div className="flex items-center gap-2 flex-1">
                        <span 
                          className="w-3 h-3 rounded-full flex-shrink-0" 
                          style={{ backgroundColor: categoryColors(cat) as string }}
                        />
                        <span className="text-white truncate">{cat}</span>
                      </div>
                      <span className="text-gray-400 ml-2">${((vol as number) / 1e6).toFixed(0)}M</span>
                    </div>
                  ));
              })()}
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}

