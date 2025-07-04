import { Component, Input } from '@angular/core';
import { TreeNode } from '../../models/tree-node.model';

@Component({
  selector: 'app-node1',
  template: `
    <div class="node-content">
      <span class="node-id">{{ node.id }}</span>
      <span class="node-title">{{ node.title }}</span>
      <button
        (click)="handleClick()"
        class="action-button">
        Нажми меня
      </button>
    </div>
  `,
  styles: [`
    .node-content {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 6px 0;
    }

    .node-id {
      font-weight: bold;
      color: #2c3e50;
      min-width: 24px;
      text-align: center;
    }

    .node-title {
      flex-grow: 1;
      color: #34495e;
    }

    .action-button {
      margin-left: 10px;
      padding: 6px 12px;
      background: linear-gradient(to bottom, #e74c3c, #c0392b);
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      font-size: 13px;
      position: relative;
      overflow: hidden;
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      box-shadow: 0 1px 2px rgba(0,0,0,0.1);
      min-width: 100px;
      text-align: center;

      &:hover:not(:disabled) {
        transform: translateY(-1px);
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
        background: linear-gradient(to bottom, #ff6b5b, #e74c3c);
      }

      &:active:not(:disabled) {
        transform: translateY(1px);
        box-shadow: none;
      }

      &::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 5px;
        height: 5px;
        background: rgba(255,255,255,0.5);
        opacity: 0;
        border-radius: 100%;
        transform: scale(1, 1) translate(-50%);
        transform-origin: 50% 50%;
      }

      &:focus:not(:disabled)::after {
        animation: ripple 0.6s ease-out;
      }
    }

    @keyframes ripple {
      0% { transform: scale(0, 0); opacity: 1; }
      100% { transform: scale(20, 20); opacity: 0; }
    }
  `]
})
export class Node1Component {
  @Input({ required: true }) node!: TreeNode;

  handleClick(): void {
    console.log(`Нажали на узел ID ${this.node.id}`);
  }
}
