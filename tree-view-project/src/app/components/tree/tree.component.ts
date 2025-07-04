import { Component, Input, Output, EventEmitter, TemplateRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TreeNode } from '../../models/tree-node.model';

@Component({
  selector: 'app-tree',
  standalone: true,
  imports: [CommonModule],
  styles: [`
    ul {
      list-style-type: none;
      padding-left: 20px;
      margin: 0;
    }

    li {
      margin: 8px 0;
      position: relative;
    }

    .node-container {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 6px 10px;
      border-radius: 6px;
      transition: all 0.3s ease;
      background-color: rgba(255, 255, 255, 0.9);

      &:hover {
        background-color: rgba(241, 243, 244, 0.9);
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
      }
    }

    .node-circle {
      width: 36px;
      height: 36px;
      border-radius: 50%;
      background: linear-gradient(135deg, #2ecc71, #27ae60);
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: bold;
      font-size: 14px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);

      &.deleted {
        background: linear-gradient(135deg, #95a5a6, #7f8c8d) !important;
      }
    }

    .node-content {
      display: flex;
      align-items: center;
      gap: 12px;
      flex-grow: 1;
    }

    .toggle-icon {
      cursor: pointer;
      font-size: 16px;
      margin-right: 8px;
      color: #3498db;
      user-select: none;
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      min-width: 16px;
      text-align: center;
      padding: 4px;

      &:hover {
        color: #2980b9;
        transform: scale(1.1);
      }
    }

    /* Анимация раскрытия дочерних узлов */
    app-tree {
      display: block;
      overflow: hidden;
      max-height: 0;
      opacity: 0;
      transform: translateY(-10px);
      transition:
        max-height 0.3s ease-out,
        opacity 0.3s ease-out,
        transform 0.3s ease-out;

      &.expanded {
        max-height: 2000px;
        opacity: 1;
        transform: translateY(0);
      }
    }

    /* Вертикальные соединительные линии */
    ul {
      position: relative;

      &::before {
        content: "";
        position: absolute;
        top: 0;
        bottom: 0;
        left: 16px;
        width: 1px;
        background: #e0e0e0;
      }
    }

    li {
      &::before {
        content: "";
        position: absolute;
        top: 24px;
        left: 16px;
        width: 12px;
        height: 1px;
        background: #e0e0e0;
      }
    }
  `],
  template: `
    <ul>
      @for (node of nodes; track node.id) {
        <li>
          <div class="node-container" [style.color]="node.is_deleted ? '#7f8c8d' : 'inherit'">
            @if (node.children && node.children.length > 0) {
              <span
                class="toggle-icon"
                (click)="toggleNode(node.id)"
                [style.transform]="isExpanded(node.id) ? 'rotate(180deg) scale(1.1)' : 'rotate(0) scale(1.1)'">
                ▼
              </span>
            } @else {
              <span class="toggle-icon" style="visibility: hidden;">▼</span>
            }

            <div class="node-content">
              <div class="node-circle" [class.deleted]="node.is_deleted">
                {{ node.id }}
              </div>
              <ng-container
                [ngTemplateOutlet]="nodeTemplate"
                [ngTemplateOutletContext]="{ $implicit: node }">
              </ng-container>
            </div>
          </div>

          @if (node.children && node.children.length > 0) {
            <app-tree
              [nodes]="node.children"
              [nodeTemplate]="nodeTemplate"
              [expandedIds]="expandedIds"
              (nodeClicked)="nodeClicked.emit($event)"
              [class.expanded]="isExpanded(node.id)">
            </app-tree>
          }
        </li>
      }
    </ul>
  `
})
export class TreeComponent {
  @Input() nodes: TreeNode[] = [];
  @Input() nodeTemplate!: TemplateRef<any>;
  @Input() expandedIds: number[] = [];
  @Output() nodeClicked = new EventEmitter<number>();

  protected isExpanded(id: number): boolean {
    return this.expandedIds.includes(id);
  }

  protected toggleNode(id: number): void {
    this.nodeClicked.emit(id);
  }
}
