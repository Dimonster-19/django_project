import { Component, Input, Output, EventEmitter } from '@angular/core';
import { TreeNode } from '../../models/tree-node.model';

@Component({
  selector: 'app-node2',
  template: `
    <div class="node-content">
      <span class="node-title">{{ node.title }}</span>
      @if (hasChildren) {
        <span class="children-count">({{ node.children!.length }})</span>
      }
      <button
        (click)="triggerExpand()"
        [disabled]="!hasChildren"
        class="expand-button">
        Развернуть всё
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

    .node-title {
      flex-grow: 1;
      color: #34495e;
    }

    .children-count {
      color: #7f8c8d;
      font-size: 0.9em;
    }

    .expand-button {
      position: relative;
      margin-left: 10px;
      padding: 6px 12px;
      background: linear-gradient(to bottom, #f39c12, #e67e22);
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      font-size: 13px;
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      overflow: hidden;
      box-shadow: 0 1px 2px rgba(0,0,0,0.1);
      min-width: 100px;
      text-align: center;

      &:hover:not(:disabled) {
        transform: translateY(-1px);
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
        background: linear-gradient(to bottom, #ffbb33, #f39c12);
      }

      &:active:not(:disabled) {
        transform: translateY(1px);
        box-shadow: none;
      }

      &:disabled {
        background: #95a5a6;
        cursor: not-allowed;
        opacity: 0.7;
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
export class Node2Component {
  @Input({ required: true }) node!: TreeNode;
  @Input() expandedIds: number[] = [];
  @Output() expandNodes = new EventEmitter<number[]>();

  get hasChildren(): boolean {
    return !!this.node.children?.length;
  }

  protected triggerExpand(): void {
    if (this.hasChildren) {
      this.expandNodes.emit(this.getAllChildIds(this.node));
    }
  }

  private getAllChildIds(node: TreeNode): number[] {
    const ids: number[] = [];
    node.children?.forEach(child => {
      ids.push(child.id);
      if (child.children?.length) {
        ids.push(...this.getAllChildIds(child));
      }
    });
    return ids;
  }
}
