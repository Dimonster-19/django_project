import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TreeNode } from './models/tree-node.model';
import { TreeComponent } from './components/tree/tree.component';
import { Node1Component } from './components/node/node1.component';
import { Node2Component } from './components/node/node2.component';

const TREE_DATA: TreeNode[] = [
  {
    id: 1,
    title: "Значение 1",
    is_deleted: false,
    children: [
      {
        id: 2,
        title: "Значение 1.1",
        is_deleted: false,
        children: [
          {
            id: 3,
            title: "Значение 1.1.1",
            is_deleted: true,
            children: []
          }
        ]
      },
      {
        id: 4,
        title: "Значение 1.2",
        is_deleted: false,
        children: [
          {
            id: 5,
            title: "Значение 1.2.1",
            is_deleted: false,
            children: []
          },
          {
            id: 6,
            title: "Значение 1.2.2",
            is_deleted: false,
            children: []
          }
        ]
      }
    ]
  },
  {
    id: 7,
    title: "Значение 2",
    is_deleted: false,
    children: [
      {
        id: 8,
        title: "Значение 2.1",
        is_deleted: true,
        children: [
          {
            id: 9,
            title: "Значение 2.1.1",
            is_deleted: true,
            children: [
              {
                id: 10,
                title: "Значение 2.1.1.1",
                is_deleted: true,
                children: [
                  {
                    id: 11,
                    title: "Значение 2.1.1.1.1",
                    is_deleted: true,
                    children: [
                      {
                        id: 12,
                        title: "Значение 2.1.1.1.1.1",
                        is_deleted: false,
                        children: [
                          {
                            id: 13,
                            title: "Значение 2.1.1.1.1.1.1",
                            is_deleted: false,
                            children: []
                          }
                        ]
                      },
                      {
                        id: 14,
                        title: "Значение 2.1.1.1.1.2",
                        is_deleted: false,
                        children: []
                      }
                    ]
                  }
                ]
              }
            ]
          }
        ]
      }
    ]
  }
];

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, TreeComponent, Node1Component, Node2Component],
  template: `
    <div class="app-container">
      <h2>Дерево 1</h2>
      <app-tree
        [nodes]="firstTreeData"
        [nodeTemplate]="node1Template"
        [expandedIds]="expandedIds1"
        (nodeClicked)="toggleNode($event, 1)">
      </app-tree>

      <h2>Дерево 2</h2>
      <app-tree
        [nodes]="secondTreeData"
        [nodeTemplate]="node2Template"
        [expandedIds]="expandedIds2"
        (nodeClicked)="toggleNode($event, 2)">
      </app-tree>

      <ng-template #node1Template let-node>
        <app-node1 [node]="node"></app-node1>
      </ng-template>

      <ng-template #node2Template let-node>
        <app-node2
          [node]="node"
          [expandedIds]="expandedIds2"
          (expandNodes)="onExpandAll2($event)">
        </app-node2>
      </ng-template>
    </div>
  `,
  styles: [`
    .app-container {
      padding: 24px;
      font-family: 'Segoe UI', Roboto, sans-serif;
      max-width: 800px;
      margin: 0 auto;
      background: #f8f9fa;
      border-radius: 12px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }

    h2 {
      color: #2c3e50;
      margin: 0 0 16px 0;
      padding-bottom: 8px;
      border-bottom: 2px solid #3498db;
      font-weight: 600;
      font-size: 1.5rem;
    }

    app-tree {
      display: block;
      margin-top: 12px;
      background: white;
      padding: 16px;
      border-radius: 8px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.05);
      transition: all 0.3s ease;

      &:hover {
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
      }
    }

    /* Анимация появления деревьев */
    app-tree {
      animation: fadeIn 0.4s ease-out forwards;
    }

    @keyframes fadeIn {
      from {
        opacity: 0;
        transform: translateY(-8px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }
  `]
})
export class AppComponent {
  firstTreeData = TREE_DATA[0].children ? [TREE_DATA[0]] : [];
  secondTreeData = TREE_DATA[1].children ? [TREE_DATA[1]] : [];

  expandedIds1: number[] = [];
  expandedIds2: number[] = [];

  toggleNode(id: number, treeNumber: number): void {
    if (treeNumber === 1) {
      this.expandedIds1 = this.expandedIds1.includes(id)
        ? this.expandedIds1.filter(i => i !== id)
        : [...this.expandedIds1, id];
    } else {
      this.expandedIds2 = this.expandedIds2.includes(id)
        ? this.expandedIds2.filter(i => i !== id)
        : [...this.expandedIds2, id];
    }
  }

  onExpandAll2(ids: number[]): void {
    const nodesWithChildren = this.collectNodesWithChildren(this.secondTreeData);
    this.expandedIds2 = [...new Set([...this.expandedIds2, ...nodesWithChildren])];
  }

  private collectNodesWithChildren(nodes: TreeNode[]): number[] {
    return nodes.reduce((acc, node) => {
      if (node.children && node.children.length > 0) {
        return [...acc, node.id, ...this.collectNodesWithChildren(node.children)];
      }
      return acc;
    }, [] as number[]);
  }
}
