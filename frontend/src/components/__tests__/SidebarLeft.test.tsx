import React from 'react';
import { render, screen } from '@testing-library/react';
import SidebarLeft from '../SidebarLeft';

describe('SidebarLeft Component - Static Tests', () => {
    it('renders the brand title correctly', () => {
        render(<SidebarLeft />);
        expect(screen.getByText('Origin Financial')).toBeInTheDocument();
    });

    it('renders all semantic navigation links', () => {
        render(<SidebarLeft />);

        // Check for specific navigation items
        expect(screen.getByText('Dashboard')).toBeInTheDocument();
        expect(screen.getByText('Recent Chats')).toBeInTheDocument();
        expect(screen.getByText('Settings')).toBeInTheDocument();

        // Check if there are exactly 3 navigation links
        const navLinks = screen.getAllByRole('link');
        expect(navLinks.length).toBe(3);
    });

    it('renders the user profile stub', () => {
        render(<SidebarLeft />);
        expect(screen.getByText('User')).toBeInTheDocument();
        expect(screen.getByText('U')).toBeInTheDocument(); // The avatar initial
    });
});
